from fastapi import APIRouter

router = APIRouter()


@router.get('/me')
def get_me() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/users/me GET'}


@router.put('/me')
def update_me() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/users/me PUT'}


@router.get('')
def list_users() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/users GET'}


@router.post('')
def create_user() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/users POST'}


@router.put('/{user_id}')
def update_user(user_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/users/{user_id} PUT'}


@router.post('/{user_id}/deactivate')
def deactivate_user(user_id: str) -> dict[str, str]:
    return {'message': f'TODO: implement /api/v1/users/{user_id}/deactivate POST'}
