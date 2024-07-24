from domains import Service
from fastapi import HTTPException, status
from dependencies.auth import hash_password, verify_password
from .repositories import UserRepository
from domains.users.dto import (
    FarmerJoinDTO
)
from domains.users.models import FarmersModel

class UserService(Service):
    def __init__(
        self,
        *,
        user_repository: UserRepository,
    ):
        self._user_repository = user_repository

    async def create_user(self, *, payload:FarmerJoinDTO) -> FarmersModel:
        payload.data.user_password = hash_password(payload.data.user_password)
        user = await self._user_repository.create_user(payload=payload)
        return user