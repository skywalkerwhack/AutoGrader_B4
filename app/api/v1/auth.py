from fastapi import APIRouter

router = APIRouter()


@router.post('/login')
def login() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/auth/login'}


@router.post('/logout')
def logout() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/auth/logout'}


@router.post('/refresh')
def refresh_token() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/auth/refresh'}


@router.post('/reset-password')
def reset_password() -> dict[str, str]:
    return {'message': 'TODO: implement /api/v1/auth/reset-password'}
