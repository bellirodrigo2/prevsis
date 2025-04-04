from datetime import date, timedelta

from pydantic import BaseModel


class File(BaseModel):
    hook_id: str
    file_name: str
    file_path: str
    version: str
    created_by: str
    created_at: date
    valid_for: timedelta
    draft: bool
