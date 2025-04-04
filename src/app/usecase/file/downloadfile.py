from app.usecase.usecase import UseCase
from domain.vo.file import File


@dataclass
class DownloadFile(UseCase):
    storage: FileStorageGateway
    repo: FileRepository
    hash: HashService

    def execute(self, file_id: str) -> tuple[File, bytes]:

        file_meta: Optional[File] = self.repo.get_by_id(file_id)

        if not file_meta:
            raise FileNotFoundError(f"File with id {file_id} not found.")

        file_bytes = self.storage.download(file_meta.file_path)

        calculated_hash = self.hash_service.generate(file_bytes)

        if calculated_hash != file_meta.file_hash:
            raise FileIntegrityError(f"Hash mismatch for file {file_id}")

        return file_meta, file_bytes
