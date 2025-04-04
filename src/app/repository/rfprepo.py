from typing import Protocol

from domain.entity.rfp import RequestForProposal


class RFPRepository(Protocol):
    def save(self, rfp: RequestForProposal) -> None: ...
