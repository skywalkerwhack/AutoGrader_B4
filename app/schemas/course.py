from pydantic import BaseModel


class CourseCreate(BaseModel):
    course_name: str
    course_code: str
    semester: str
    description: str | None = None
