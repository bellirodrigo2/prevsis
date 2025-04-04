from datetime import date
from enum import Enum

from pydantic import BaseModel


class RecurrenceType(str, Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class FUPItem(BaseModel):
    id: str
    job_id: str
    title: str
    description: str
    created_at: date
    until: date
    recurrence: RecurrenceType
    recurrence_count: int
    msg_method: str
