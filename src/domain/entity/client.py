from typing import Optional

from pydantic import BaseModel, EmailStr

from domain.vo.address import Address
from domain.vo.cpf import CPF
from domain.vo.personname import Name


class Client(BaseModel):
    id: str
    name: Name
    # adicionar campo business
    email: EmailStr
    phone: Optional[str] = None
    cpf: Optional[CPF] = None
    addr: Optional[Address] = None
