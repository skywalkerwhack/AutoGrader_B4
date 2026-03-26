from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate
from app.services import course_service

router = APIRouter()


class CurrentUser:
    def __init__(self, user_id: int, role: str) -> None:
        self.user_id = user_id
        self.role = role


def get_current_user(
    x_user_id: Annotated[int | None, Header()] = None,
    x_user_role: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    if x_user_id is None or x_user_role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing authentication headers: X-User-Id and X-User-Role',
        )
    return CurrentUser(user_id=x_user_id, role=x_user_role)


@router.get('', response_model=list[CourseOut])
def list_courses(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    teacher_id: int | None = Query(default=None),
    semester: str | None = Query(default=None),
) -> list[CourseOut]:
    return course_service.list_courses(
        db=db,
        user_id=current_user.user_id,
        role=current_user.role,
        teacher_id=teacher_id,
        semester=semester,
    )


@router.post('', response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> CourseOut:
    if current_user.role != 'Teacher':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only teachers can create courses')
    return course_service.create_course(db=db, payload=payload, teacher_user_id=current_user.user_id)


@router.get('/{course_id}', response_model=CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> CourseOut:
    course = course_service.get_course_or_404(db, course_id)
    course_service.ensure_course_access(db, course, current_user.user_id, current_user.role)
    return course


@router.put('/{course_id}', response_model=CourseOut)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> CourseOut:
    if current_user.role != 'Teacher':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only teachers can update courses')
    course = course_service.get_course_or_404(db, course_id)
    if course.teacher_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only course creator can update course')
    return course_service.update_course(db, course, payload)


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    if current_user.role != 'Teacher':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only teachers can delete courses')
    course = course_service.get_course_or_404(db, course_id)
    if course.teacher_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only course creator can delete course')
    course_service.ensure_course_deletable(db, course_id)
    course_service.delete_course(db, course)
