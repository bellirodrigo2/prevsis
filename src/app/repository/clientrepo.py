from dataclasses import dataclass
from typing import Optional, Protocol, Sequence

from domain.entity.client import Client


@dataclass
class ClientAlreadyExistsError(Exception):
    field: str
    value: str

    def __post_init__(self) -> None:
        super().__init__(f"Já existe um cliente com o mesmo {self.field}: {self.value}")


class ClientRepository(Protocol):
    def save(self, client: Client) -> None: ...

    def search(
        self,
        *,
        name_contains: Optional[str] = None,
        email_contains: Optional[str] = None,
        cpf_contains: Optional[str] = None,
    ) -> Sequence[Client]: ...
