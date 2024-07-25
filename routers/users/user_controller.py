from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.database import provide_session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from domains.users.services import UserService
from domains.users.repositories import UserRepository
from domains.users.dto import (
    FarmerJoinDTO,
    UserLoginDTO,
    Token
)
from domains.users.models import FarmersModel
import logging

logger = logging.getLogger(__name__)


router = APIRouter()

name = "users"

@router.post(f"/{name}/join")
async def create_user(payload: FarmerJoinDTO, db=Depends(provide_session)):
    print(payload)
    user_service = UserService(user_repository=UserRepository(session=db))
    user_name = await user_service.create_user(payload=payload)
    return user_name

@router.post(f"/{name}/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(provide_session)):
    logger.debug(f"Login attempt for user: {form_data.username}")
    
    user_service = UserService(user_repository=UserRepository(session=db))
    
    try:
        login_data = UserLoginDTO(username=form_data.username, password=form_data.password)
        token = await user_service.login(login_data)
        logger.info(f"Login successful for user: {form_data.username}")
        return token
    except HTTPException as he:
        logger.warning(f"Login failed for user {form_data.username}: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"An unexpected error occurred during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login",
        )
        
@router.get(f"/{name}/me")
async def read_users_me(current_user: FarmersModel = Depends(UserService.get_current_user)):
    return current_user