from datetime import datetime

from sqlalchemy import Select, delete, select
from sqlalchemy.orm import Session

from app.models.assignment import Assignment, AssignmentQuestion
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate


def list_assignments(
    db: Session,
    *,
    class_id: int | None = None,
    teacher_id: int | None = None,
    is_published: bool | None = None,
) -> list[Assignment]:
    stmt: Select[tuple[Assignment]] = select(Assignment)
    if class_id is not None:
        stmt = stmt.where(Assignment.class_id == class_id)
    if teacher_id is not None:
        stmt = stmt.where(Assignment.teacher_id == teacher_id)
    if is_published is not None:
        stmt = stmt.where(Assignment.is_published == is_published)
    stmt = stmt.order_by(Assignment.created_at.desc())
    return list(db.scalars(stmt).all())


def get_assignment_by_id(db: Session, assignment_id: int) -> Assignment | None:
    return db.get(Assignment, assignment_id)


def list_assignment_questions(db: Session, assignment_id: int) -> list[str]:
    stmt: Select[tuple[AssignmentQuestion]] = (
        select(AssignmentQuestion)
        .where(AssignmentQuestion.assignment_id == assignment_id)
        .order_by(AssignmentQuestion.order_index.asc())
    )
    return [row.question_id for row in db.scalars(stmt).all()]


def create_assignment(db: Session, payload: AssignmentCreate) -> Assignment:
    assignment = Assignment(
        title=payload.title,
        description=payload.description,
        class_id=payload.class_id,
        teacher_id=payload.teacher_id,
        due_date=payload.due_date,
        is_published=payload.is_published,
        allow_resubmit=payload.allow_resubmit,
        published_at=datetime.utcnow() if payload.is_published else None,
    )
    db.add(assignment)
    db.flush()

    for index, question_id in enumerate(payload.questions):
        db.add(
            AssignmentQuestion(
                assignment_id=assignment.assignment_id,
                question_id=question_id,
                order_index=index,
            )
        )

    db.commit()
    db.refresh(assignment)
    return assignment


def update_assignment(db: Session, assignment: Assignment, payload: AssignmentUpdate) -> Assignment:
    update_data = payload.model_dump(exclude_unset=True)
    questions = update_data.pop('questions', None)

    for field, value in update_data.items():
        setattr(assignment, field, value)

    db.add(assignment)

    if questions is not None:
        db.execute(
            delete(AssignmentQuestion).where(AssignmentQuestion.assignment_id == assignment.assignment_id)
        )
        for index, question_id in enumerate(questions):
            db.add(
                AssignmentQuestion(
                    assignment_id=assignment.assignment_id,
                    question_id=question_id,
                    order_index=index,
                )
            )

    db.commit()
    db.refresh(assignment)
    return assignment


def publish_assignment(db: Session, assignment: Assignment) -> Assignment:
    if not assignment.is_published:
        assignment.is_published = True
        assignment.published_at = datetime.utcnow()
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
    return assignment
