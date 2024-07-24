from fastapi import APIRouter, Depends
from dependencies.database import provide_session

from domains.users.services import UserService
from domains.users.repositories import UserRepository
from domains.users.dto import (
    FarmerJoinDTO
)
router = APIRouter()

name = "users"

@router.post(f"/{name}/join")
async def create_user(payload: FarmerJoinDTO, db=Depends(provide_session)):
    print(payload)
    user_service = UserService(user_repository=UserRepository(session=db))
    user_name = await user_service.create_user(payload=payload)
    return user_name