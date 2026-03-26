from fastapi import APIRouter

router = APIRouter()


@router.get('/my')
def my_grades() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/grades/my GET'}


@router.get('/class/{class_id}')
def class_grades(class_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/grades/class/{class_id} GET'}


@router.get('/export/{assignment_id}')
def export_grades(assignment_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/grades/export/{assignment_id} GET'}
