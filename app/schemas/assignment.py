from datetime import datetime

from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    title: str
    class_id: int
    questions: list[str]
    due_date: datetime
    is_published: bool = False
