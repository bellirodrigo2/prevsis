from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.database.mixins import TimestampMixin
from infra.database.models.base import Base


class AddressModel(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column(String(100))
    number: Mapped[str] = mapped_column(String(20))
    neighborhood: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(2))
    zip_code: Mapped[str] = mapped_column(String(10))


class ClientModel(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str | None]
    cpf: Mapped[str | None]

    address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id"), nullable=True
    )
    addr: Mapped[AddressModel | None] = relationship()

    rfps = relationship(
        "RFPModel", back_populates="client", cascade="all, delete-orphan"
    )
