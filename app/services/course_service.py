from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def list_courses(
    db: Session,
    *,
    teacher_id: int | None = None,
    semester: str | None = None,
) -> list[Course]:
    stmt: Select[tuple[Course]] = select(Course)
    if teacher_id is not None:
        stmt = stmt.where(Course.teacher_id == teacher_id)
    if semester is not None:
        stmt = stmt.where(Course.semester == semester)
    stmt = stmt.order_by(Course.created_at.desc())
    return list(db.scalars(stmt).all())


def get_course_by_id(db: Session, course_id: int) -> Course | None:
    return db.get(Course, course_id)


def find_course_by_code_and_semester(
    db: Session,
    *,
    course_code: str,
    semester: str,
) -> Course | None:
    stmt: Select[tuple[Course]] = select(Course).where(
        Course.course_code == course_code,
        Course.semester == semester,
    )
    return db.scalars(stmt).first()


def create_course(db: Session, payload: CourseCreate) -> Course:
    course = Course(
        course_name=payload.course_name,
        course_code=payload.course_code,
        semester=payload.semester,
        description=payload.description,
        teacher_id=payload.teacher_id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course: Course, payload: CourseUpdate) -> Course:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course: Course) -> None:
    db.delete(course)
    db.commit()
