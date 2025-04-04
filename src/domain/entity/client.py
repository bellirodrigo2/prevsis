from email.headerregistry import Address
from typing import Optional

from pydantic import BaseModel, EmailStr

from domain.vo.cpf import CPF


class Client(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    cpf: Optional[CPF] = None
    addr: Optional[Address] = None
