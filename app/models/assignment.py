from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Assignment(Base):
    __tablename__ = 'assignments'

    assignment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    class_id: Mapped[int] = mapped_column(ForeignKey('classes.class_id'), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_resubmit: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AssignmentQuestion(Base):
    __tablename__ = 'assignment_questions'

    assignment_id: Mapped[int] = mapped_column(ForeignKey('assignments.assignment_id'), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
