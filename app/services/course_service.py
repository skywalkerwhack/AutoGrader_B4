from fastapi import HTTPException, status
from sqlalchemy import Select, exists, select
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.class_model import Class, ClassStudent
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def list_courses(
    db: Session,
    user_id: int,
    role: str,
    teacher_id: int | None = None,
    semester: str | None = None,
) -> list[Course]:
    stmt: Select[tuple[Course]] = select(Course)

    if role == 'Teacher':
        effective_teacher_id = teacher_id if teacher_id is not None else user_id
        if effective_teacher_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Teacher can only query own courses')
        stmt = stmt.where(Course.teacher_id == user_id)
    else:
        joined_course_exists = (
            select(Class.class_id)
            .join(ClassStudent, ClassStudent.class_id == Class.class_id)
            .where(Class.course_id == Course.course_id, ClassStudent.student_user_id == user_id)
            .exists()
        )
        stmt = stmt.where(joined_course_exists)

    if semester:
        stmt = stmt.where(Course.semester == semester)

    return db.scalars(stmt.order_by(Course.created_at.desc(), Course.course_id.desc())).all()


def create_course(db: Session, payload: CourseCreate, teacher_user_id: int) -> Course:
    course = Course(
        course_name=payload.course_name,
        course_code=payload.course_code,
        semester=payload.semester,
        description=payload.description,
        teacher_id=teacher_user_id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_or_404(db: Session, course_id: int) -> Course:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
    return course


def ensure_course_access(db: Session, course: Course, user_id: int, role: str) -> None:
    if role == 'Teacher':
        if course.teacher_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permission to access this course')
        return

    is_joined = db.scalar(
        select(
            exists().where(
                Class.course_id == course.course_id,
                ClassStudent.class_id == Class.class_id,
                ClassStudent.student_user_id == user_id,
            )
        )
    )
    if not is_joined:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permission to access this course')


def update_course(db: Session, course: Course, payload: CourseUpdate) -> Course:
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(course, field, value)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def ensure_course_deletable(db: Session, course_id: int) -> None:
    has_published_assignment = db.scalar(
        select(
            exists().where(
                Class.course_id == course_id,
                Assignment.class_id == Class.class_id,
                Assignment.is_published.is_(True),
            )
        )
    )
    if has_published_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete course with published assignments',
        )


def delete_course(db: Session, course: Course) -> None:
    db.delete(course)
    db.commit()
