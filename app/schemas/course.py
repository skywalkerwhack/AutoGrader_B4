from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    course_name: str = Field(min_length=1, max_length=100)
    course_code: str = Field(min_length=1, max_length=30)
    semester: str = Field(min_length=1, max_length=30)
    description: str | None = None
    teacher_id: int


class CourseUpdate(BaseModel):
    course_name: str | None = Field(default=None, min_length=1, max_length=100)
    course_code: str | None = Field(default=None, min_length=1, max_length=30)
    semester: str | None = Field(default=None, min_length=1, max_length=30)
    description: str | None = None


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    course_id: int
    course_name: str
    course_code: str
    semester: str
    description: str | None
    teacher_id: int
    created_at: datetime
