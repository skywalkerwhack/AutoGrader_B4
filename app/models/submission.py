from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Submission(Base):
    __tablename__ = 'submissions'

    submission_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    student_user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    question_id: Mapped[str] = mapped_column(String(100), nullable=False)
    assignment_id: Mapped[int] = mapped_column(ForeignKey('assignments.assignment_id'), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(30), default='python')
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    passed_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overall_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    static_issues: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    case_results: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    teacher_score_override: Mapped[float | None] = mapped_column(Float, nullable=True)
    override_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
