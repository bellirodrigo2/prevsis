from typing import Optional, Protocol, Sequence

from domain.entity.client import Client


class ClientAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Já existe um cliente com o mesmo {field}: {value}")


class ClientRepository(Protocol):
    def save(self, client: Client) -> None: ...

    def search(
        self,
        *,
        name_contains: Optional[str] = None,
        email_contains: Optional[str] = None,
        cpf_contains: Optional[str] = None,
    ) -> Sequence[Client]: ...
