from dataclasses import dataclass
from email.headerregistry import Address
from typing import Optional

from pydantic import EmailStr, TypeAdapter

from app.repository.clientrepo import ClientRepository
from app.usecase.usecase import UseCase
from domain.entity.client import Client
from domain.vo.cpf import cpf_validator
from domain.vo.personname import name_validator


@dataclass
class CreateClient(UseCase):
    repo: ClientRepository

    def execute(
        self,
        *,
        name: str,
        email: str,
        phone: Optional[str] = None,
        cpf: Optional[str] = None,
        addr: Optional[Address] = None,
    ) -> Client:
        nome = name_validator(name)
        email_obj = TypeAdapter(EmailStr).validate_python(email)
        cpf_obj = cpf_validator(cpf) if cpf else None

        client = Client(
            id=-1,  # será sobrescrito no repositório após persistência
            name=nome,
            email=email_obj,
            phone=phone,
            cpf=cpf_obj,
            addr=addr,
        )

        self.repo.save(client)
        return client
