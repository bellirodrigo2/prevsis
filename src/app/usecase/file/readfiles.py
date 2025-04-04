from app.usecase.usecase import UseCase
from domain.vo.file import File


@dataclass
class ReadFiles(UseCase):
    repo: FileRepository

    def execute(self, hook_id: str) -> list[File]:

        return self.repo.get_files(hook_id)
