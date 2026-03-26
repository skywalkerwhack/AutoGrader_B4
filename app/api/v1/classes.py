from fastapi import APIRouter

router = APIRouter()


@router.get('')
def list_classes() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/classes GET'}


@router.post('')
def create_class() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/classes POST'}


@router.get('/{class_id}/students')
def list_class_students(class_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/classes/{class_id}/students GET'}


@router.post('/{class_id}/students')
def add_student_to_class(class_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/classes/{class_id}/students POST'}


@router.post('/{class_id}/students/import')
def import_students(class_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/classes/{class_id}/students/import POST'}


@router.delete('/{class_id}/students/{student_id}')
def remove_student_from_class(class_id: str, student_id: str) -> dict[str, str]:
    return {
        'message': f'TODO: implement /api/v1/classes/{class_id}/students/{student_id} DELETE'
    }
