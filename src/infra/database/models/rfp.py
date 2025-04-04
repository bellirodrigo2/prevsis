from datetime import date
from typing import Optional

from sqlalchemy import Date, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entity.rfp import RFP_Status
from infra.database.models.base import Base


class RFPModel(Base):
    __tablename__ = "rfps"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False)
    service: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    issued_at: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[RFP_Status] = mapped_column(Enum(RFP_Status), nullable=False)

    client: Mapped["ClientModel"] = relationship(back_populates="rfps")
    # job: Mapped[Optional["JobModel"]] = relationship(
    # back_populates="rfp", uselist=False
    # )
