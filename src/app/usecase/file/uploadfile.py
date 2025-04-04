from dataclasses import dataclass
from datetime import timedelta
from typing import Annotated

from app.usecase.usecase import UseCase

file_path = Annotated[str, "file_path"]
version = Annotated[str, "version"]


@dataclass
class UploadFile(UseCase):
    storage: FileStorageGateway
    repo: FileRepository
    hash: HashService

    def execute(
        self,
        hook_id: str,
        file_bytes: bytes,
        file_name: str,
        valid_for: timedelta,
        draft: bool = False,
    ) -> None:

        hash = self.hash.generate_hash(file_bytes)

        path = self.storage.save_file_bytes(file_bytes)
        self.storage.save_file(hook_id, file_name, path, valid_for, draft)
