from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.repository.rfprepo import RFPRepository
from domain.entity.rfp import RequestForProposal
from infra.database.models.rfp import RFPModel  # SQLAlchemy model


@dataclass
class SQLAlchemyRFPAdapter(RFPRepository):
    session: Session

    def save(self, rfp: RequestForProposal) -> None:
        model = RFPModel(
            id=rfp.id,
            client_id=rfp.client_id,
            service=rfp.service,
            title=rfp.title,
            description=rfp.description,
            budget=rfp.budget,
            issued_at=rfp.issued_at,
            valid_until=rfp.valid_until,
            file_path=rfp.file_path,
            status=rfp.status.value if hasattr(rfp.status, "value") else rfp.status,
        )
        self.session.add(model)
        self.session.commit()
