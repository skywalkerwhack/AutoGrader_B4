from fastapi import APIRouter

from app.api.v1 import assignments, auth, classes, courses, grades, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
api_router.include_router(grades.router, prefix="/grades", tags=["grades"])
