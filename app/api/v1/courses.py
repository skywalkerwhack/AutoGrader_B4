from fastapi import APIRouter

router = APIRouter()


@router.get('')
def list_courses() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/courses GET'}


@router.post('')
def create_course() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/courses POST'}


@router.get('/{course_id}')
def get_course(course_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/courses/{course_id} GET'}


@router.put('/{course_id}')
def update_course(course_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/courses/{course_id} PUT'}


@router.delete('/{course_id}')
def delete_course(course_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/courses/{course_id} DELETE'}
