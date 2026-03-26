from fastapi import APIRouter

router = APIRouter()


@router.get('')
def list_assignments() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/assignments GET'}


@router.post('')
def create_assignment() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/assignments POST'}


@router.put('/{assignment_id}')
def update_assignment(assignment_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/assignments/{assignment_id} PUT'}


@router.post('/{assignment_id}/publish')
def publish_assignment(assignment_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/assignments/{assignment_id}/publish POST'}
