from pydantic import BaseModel


class ClassCreate(BaseModel):
    course_id: int
    class_name: str
    class_code: str
