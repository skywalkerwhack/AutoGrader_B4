from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Teacher(Base):
    __tablename__ = 'teachers'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    teacher_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
