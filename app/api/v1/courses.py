from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services.course_service import (
    create_course,
    delete_course,
    find_course_by_code_and_semester,
    get_course_by_id,
    list_courses,
    update_course,
)

router = APIRouter()


@router.get('', response_model=list[CourseRead])
def list_courses_endpoint(
    teacher_id: int | None = Query(default=None),
    semester: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[CourseRead]:
    return list_courses(db, teacher_id=teacher_id, semester=semester)


@router.post('', response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course_endpoint(
    payload: CourseCreate,
    db: Session = Depends(get_db),
) -> CourseRead:
    existing = find_course_by_code_and_semester(
        db,
        course_code=payload.course_code,
        semester=payload.semester,
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='course_code already exists in the same semester',
        )
    return create_course(db, payload)


@router.get('/{course_id}', response_model=CourseRead)
def get_course_endpoint(course_id: int, db: Session = Depends(get_db)) -> CourseRead:
    course = get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='course not found')
    return course


@router.put('/{course_id}', response_model=CourseRead)
def update_course_endpoint(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
) -> CourseRead:
    course = get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='course not found')

    next_code = payload.course_code or course.course_code
    next_semester = payload.semester or course.semester
    duplicate = find_course_by_code_and_semester(
        db,
        course_code=next_code,
        semester=next_semester,
    )
    if duplicate is not None and duplicate.course_id != course.course_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='course_code already exists in the same semester',
        )

    return update_course(db, course, payload)


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db)) -> None:
    course = get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='course not found')
    delete_course(db, course)
