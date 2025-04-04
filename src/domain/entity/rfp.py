from datetime import date
from enum import Enum

from pydantic import BaseModel

# class Service(Enum):
#     CADRI = "cadri"
#     LICENCA = "licenciamento"
#     VISTORIA = "vistoria"


class RFP_Status(str, Enum):
    PENDENTE = "pendente"
    CANCELADA = "cancelada"
    ACEITA = "aceita"
    REJEITADA = "rejeitada"
    VENCIDA = "vencida"


class RequestForProposal(BaseModel):
    id: str
    service: str  # cadri, licenciamento, vistoria
    title: str
    description: str
    budget: float
    issued_at: date
    valid_until: date
    file_path: str
    client_id: int
    status: RFP_Status
