from pydantic import BaseModel


class GradeOverview(BaseModel):
    assignment_id: int
    total_score: float
