from datetime import datetime

from pydantic import BaseModel


class CourseCreate(BaseModel):
    course_name: str
    course_code: str
    semester: str
    description: str | None = None


class CourseUpdate(BaseModel):
    course_name: str | None = None
    course_code: str | None = None
    semester: str | None = None
    description: str | None = None


class CourseOut(BaseModel):
    course_id: int
    course_name: str
    course_code: str
    teacher_id: int
    semester: str
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
