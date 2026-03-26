from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Student(Base):
    __tablename__ = 'students'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_password_changed: Mapped[bool] = mapped_column(Boolean, default=False)
