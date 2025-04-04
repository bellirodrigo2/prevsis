from email.headerregistry import Address
from typing import Optional

from pydantic import BaseModel, EmailStr

from domain.vo.cpf import CPF
from domain.vo.personname import Name


class Client(BaseModel):
    id: int
    name: Name
    email: EmailStr
    phone: Optional[str] = None
    cpf: Optional[CPF] = None
    addr: Optional[Address] = None
