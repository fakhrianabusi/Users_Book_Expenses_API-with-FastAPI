from fastapi import APIRouter
from pydantic import BaseModel

from database import users


class UserPublic(BaseModel):
    id: int
    username: str


router = APIRouter(tags=["Users"])


@router.get("/users/{id}", response_model=UserPublic)
def users_details(id: int):
    for user in users:
        if user["id"] == id:
            return user
