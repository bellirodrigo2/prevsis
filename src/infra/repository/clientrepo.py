from dataclasses import dataclass
from typing import Optional, Sequence

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.repository.clientrepo import ClientAlreadyExistsError, ClientRepository
from domain.entity.client import Client
from domain.vo.address import Address  # se estiver em outro módulo
from infra.database.models.client import AddressModel, ClientModel


@dataclass
class SQLAlchemyClientAdapter(ClientRepository):
    session: Session

    def save(self, client: Client) -> None:
        stmt = select(ClientModel).where(
            or_(
                ClientModel.email == str(client.email),
                ClientModel.name == str(client.name),
                ClientModel.cpf == (str(client.cpf) if client.cpf else None),
            )
        )

        for existing in self.session.scalars(stmt):
            if existing.email == str(client.email):
                raise ClientAlreadyExistsError("email", client.email)
            if existing.name == str(client.name):
                raise ClientAlreadyExistsError("name", client.name)
            if existing.cpf and existing.cpf == str(client.cpf):
                raise ClientAlreadyExistsError("cpf", client.cpf)  # type: ignore

        address_model = None
        if client.addr:
            address_model = AddressModel(
                street=client.addr.street,
                number=client.addr.number,
                neighborhood=client.addr.neighborhood,
                city=client.addr.city,
                state=client.addr.state,
                zip_code=client.addr.zip_code,
            )
            self.session.add(address_model)
            self.session.flush()

        client_model = ClientModel(
            name=str(client.name),
            email=str(client.email),
            phone=client.phone,
            cpf=str(client.cpf) if client.cpf else None,
            address_id=address_model.id if address_model else None,
        )

        self.session.add(client_model)
        self.session.flush()

        client.id = client_model.id

    def search(
        self,
        *,
        name_contains: Optional[str] = None,
        email_contains: Optional[str] = None,
        cpf_contains: Optional[str] = None,
    ) -> Sequence[Client]:
        stmt = select(ClientModel).join(AddressModel, isouter=True)

        if name_contains:
            stmt = stmt.where(ClientModel.name.ilike(f"%{name_contains}%"))
        if email_contains:
            stmt = stmt.where(ClientModel.email.ilike(f"%{email_contains}%"))
        if cpf_contains:
            stmt = stmt.where(ClientModel.cpf.ilike(f"%{cpf_contains}%"))

        results: list[Client] = []
        for row in self.session.scalars(stmt):
            addr_model = row.addr
            addr = None
            if addr_model:
                addr = Address(
                    street=addr_model.street,
                    number=addr_model.number,
                    neighborhood=addr_model.neighborhood,
                    city=addr_model.city,
                    state=addr_model.state,
                    zip_code=addr_model.zip_code,
                )

            client = Client(
                id=row.id,
                name=row.name,
                email=row.email,
                phone=row.phone,
                cpf=row.cpf,
                addr=addr,
            )
            results.append(client)

        return results
