from datetime import date
from enum import Enum

from pydantic import BaseModel

from domain.vo.file import File

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
    client_id: int
    service: str  # cadri, licenciamento, vistoria
    title: str
    description: str
    budget: float
    issued_at: date
    files: list[File]
    _status: RFP_Status

    @property
    def file(self) -> File | None:
        non_draft_files = [f for f in self.files if not f.draft]
        return (
            None
            if not non_draft_files
            else max(non_draft_files, key=lambda f: f.created_at)
        )

    @property
    def status(self) -> RFP_Status:
        if (
            self._status == RFP_Status.PENDENTE
            and (f := self.file)
            and (f.created_at + f.valid_for < date.today())
        ):
            return RFP_Status.VENCIDA

        return self._status
