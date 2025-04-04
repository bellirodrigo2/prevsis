import uuid
from dataclasses import dataclass

from app.repository.rfprepo import RFPRepository
from domain.entity.rfp import RequestForProposal


@dataclass
class CreateRFPUseCase:
    repo: RFPRepository

    def execute(self, data: RequestForProposal) -> RequestForProposal:
        rfp = RequestForProposal(
            id=str(uuid.uuid4()),
            client_id=data.client_id,
            service=data.service,
            title=data.title,
            description=data.description,
            budget=data.budget,
            issued_at=data.issued_at,
            valid_until=data.valid_until,
            file_path=data.file_path,
            status="pendente",  # ou RFP_Status.PENDENTE se for Enum
        )
        self.repo.save(rfp)
        return rfp
