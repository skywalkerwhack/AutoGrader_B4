from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.assignment import AssignmentCreate, AssignmentRead, AssignmentUpdate
from app.services.assignment_service import (
    create_assignment,
    get_assignment_by_id,
    list_assignment_questions,
    list_assignments,
    publish_assignment,
    update_assignment,
)

router = APIRouter()


def _to_assignment_read(db: Session, assignment) -> AssignmentRead:
    return AssignmentRead(
        assignment_id=assignment.assignment_id,
        title=assignment.title,
        description=assignment.description,
        class_id=assignment.class_id,
        teacher_id=assignment.teacher_id,
        due_date=assignment.due_date,
        is_published=assignment.is_published,
        allow_resubmit=assignment.allow_resubmit,
        created_at=assignment.created_at,
        published_at=assignment.published_at,
        questions=list_assignment_questions(db, assignment.assignment_id),
    )


@router.get('', response_model=list[AssignmentRead])
def list_assignments_endpoint(
    class_id: int | None = Query(default=None),
    teacher_id: int | None = Query(default=None),
    is_published: bool | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[AssignmentRead]:
    assignments = list_assignments(
        db,
        class_id=class_id,
        teacher_id=teacher_id,
        is_published=is_published,
    )
    return [_to_assignment_read(db, assignment) for assignment in assignments]


@router.post('', response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
def create_assignment_endpoint(payload: AssignmentCreate, db: Session = Depends(get_db)) -> AssignmentRead:
    assignment = create_assignment(db, payload)
    return _to_assignment_read(db, assignment)


@router.put('/{assignment_id}', response_model=AssignmentRead)
def update_assignment_endpoint(
    assignment_id: int,
    payload: AssignmentUpdate,
    db: Session = Depends(get_db),
) -> AssignmentRead:
    assignment = get_assignment_by_id(db, assignment_id)
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='assignment not found')

    assignment = update_assignment(db, assignment, payload)
    return _to_assignment_read(db, assignment)


@router.post('/{assignment_id}/publish', response_model=AssignmentRead)
def publish_assignment_endpoint(assignment_id: int, db: Session = Depends(get_db)) -> AssignmentRead:
    assignment = get_assignment_by_id(db, assignment_id)
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='assignment not found')

    assignment = publish_assignment(db, assignment)
    return _to_assignment_read(db, assignment)
