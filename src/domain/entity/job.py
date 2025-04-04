from datetime import date

from pydantic import BaseModel

from domain.entity.fupitem import FUPItem


class Job(BaseModel):
    id: str
    rfp_id: str
    client_id: int
    title: str
    start_at: date
    file_path: str
    follow_up_items: list[FUPItem]
