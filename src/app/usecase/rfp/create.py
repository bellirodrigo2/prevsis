import uuid
from dataclasses import dataclass
from typing import Callable

from app.repository.rfprepo import RFPRepository
from app.usecase.usecase import UseCase
from domain.entity.rfp import RequestForProposal


@dataclass
class CreateRFP(UseCase):
    repo: RFPRepository
    makeid: Callable[[], str]

    def execute(self, data: RequestForProposal) -> RequestForProposal:

        id = self.makeid()
        rfp = RequestForProposal(
            id=id,
            client_id=data.client_id,
            service=data.service,
            title=data.title,
            description=data.description,
            budget=data.budget,
            issued_at=data.issued_at,
            _status="pendente",  # ou RFP_Status.PENDENTE se for Enum
        )
        self.repo.save(rfp)
        return rfp

    id: str
    client_id: int
    service: str  # cadri, licenciamento, vistoria
    title: str
    description: str
    budget: float
    issued_at: date
    files: list[File]
    _status: RFP_Status
