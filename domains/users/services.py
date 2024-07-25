from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from domains.users.repositories import UserRepository
from domains.users.dto import FarmerJoinDTO, UserLoginDTO, Token
from domains.users.models import FarmersModel

# 이 값들은 환경 변수나 설정 파일에서 가져오는 것이 좋습니다.
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def create_user(self, payload: FarmerJoinDTO) -> FarmersModel:
        # 비밀번호 해싱
        hashed_password = self._hash_password(payload.data.user_password)
        payload.data.user_password = hashed_password
        return await self._user_repository.create_user(payload=payload)

    async def authenticate_user(self, username: str, password: str) -> Optional[FarmersModel]:
        user = await self._user_repository.get_user_by_username(username)
        if not user:
            return None
        if not self._verify_password(password, user.user_password):
            return None
        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> FarmersModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await self._user_repository.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def login(self, login_data: UserLoginDTO) -> Token:
        user = await self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(data={"sub": str(user.user_id_farmer)})
        return Token(token=access_token, type="bearer")


    async def get_user_profile(self, user: FarmersModel) -> dict:
        # 필요에 따라 사용자 프로필 정보를 반환합니다.
        return {
            "user_id": user.user_id_farmer,
            "email": user.user_email,
            "name": user.user_name,
            "user_type": user.user_type,
            # 필요한 다른 필드들을 추가할 수 있습니다.
        }
