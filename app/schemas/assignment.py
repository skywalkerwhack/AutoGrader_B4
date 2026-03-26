from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    class_id: int
    teacher_id: int
    questions: list[str] = Field(default_factory=list)
    due_date: datetime
    is_published: bool = False
    allow_resubmit: bool = True


class AssignmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    due_date: datetime | None = None
    questions: list[str] | None = None
    allow_resubmit: bool | None = None


class AssignmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    assignment_id: int
    title: str
    description: str | None
    class_id: int
    teacher_id: int
    due_date: datetime
    is_published: bool
    allow_resubmit: bool
    created_at: datetime
    published_at: datetime | None
    questions: list[str]
