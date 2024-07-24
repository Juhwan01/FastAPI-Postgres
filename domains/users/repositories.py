from sqlalchemy.orm import Session
from .models import FarmersModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select
from domains.users.dto import (
    FarmerJoinDTO
)
from domains.users.models import FarmersModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, payload: FarmerJoinDTO) -> FarmersModel:
        async with self._session.begin():
            # DTO에서 데이터 추출
            data = payload.data
            farmer_entity = FarmersModel(
                user_id_farmer=data.user_id_farmer,
                user_email=data.user_email,
                user_password=data.user_password,
                user_name=data.user_name,
                user_birth=data.user_birth,
                user_type=data.user_type,
                phone_number=data.phone_number,
                address=data.address,
                city=data.city,
                state=data.state,
                postal_code=data.postal_code,
                farm_address=data.farm_address,
                animal_types=data.animal_types,
                license_number_farmer=data.license_number_farmer
            )
            self._session.add(farmer_entity)
            try:
                await self._session.commit()
            except IntegrityError as e:
                # 트랜잭션 롤백 및 예외 처리
                await self._session.rollback()
                raise HTTPException(status_code=400, detail="Database integrity error: " + str(e))
            return farmer_entity