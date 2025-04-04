from dataclasses import dataclass
from email.headerregistry import Address
from typing import Callable, Optional

from pydantic import EmailStr, TypeAdapter

from app.repository.clientrepo import ClientAlreadyExistsError, ClientRepository
from app.usecase.usecase import UseCase
from domain.entity.client import Client
from domain.vo.cpf import cpf_validator
from domain.vo.personname import name_validator


@dataclass
class CreateClient(UseCase):
    repo: ClientRepository
    makeid: Callable[[], str]

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
            id=self.makeid(),
            name=nome,
            email=email_obj,
            phone=phone,
            cpf=cpf_obj,
            addr=addr,
        )

        try:
            self.repo.save(client)
        except ClientAlreadyExistsError as e:
            raise e  # ou fazer log, ou mapear para outro erro de camada superior
        except Exception as e:
            raise Exception(f"Erro ao salvar cliente: {e}") from e

        return client
