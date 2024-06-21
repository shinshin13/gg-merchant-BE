from fastapi import APIRouter

from models.user import User


router = APIRouter(prefix = "/users")

@router.get("/")
def get_all() -> list[User]:
    return [
        User(id = 1, name = "Test user 1"),
        User(id = 2, name = "Test user 2")
    ]
