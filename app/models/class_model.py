from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Class(Base):
    __tablename__ = 'classes'

    class_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.course_id'), nullable=False)
    class_name: Mapped[str] = mapped_column(String(100), nullable=False)
    class_code: Mapped[str] = mapped_column(String(30), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ClassStudent(Base):
    __tablename__ = 'class_students'

    class_id: Mapped[int] = mapped_column(ForeignKey('classes.class_id'), primary_key=True)
    student_user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
