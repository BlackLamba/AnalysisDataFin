from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.schemas.user_schema import UserCreate
import uuid


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate) -> UserModel:
        db_user = UserModel(
            LastName=user_data.last_name,
            FirstName=user_data.first_name,
            MiddleName=user_data.middle_name,
            PassportNumber=user_data.passport_number,
            Email=user_data.email,
            hashed_password=get_password_hash(user_data.password.get_secret_value()),
            # RegistrationDate добавится автоматически через server_default
        )

        try:
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            await self.db.rollback()
            if "unique constraint" in str(e).lower():
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            raise HTTPException(
                status_code=500,
                detail="Database error"
            )

    async def get(self, user_id: str) -> UserModel | None:
        try:
            result = await self.db.execute(
                select(UserModel).where(UserModel.UserID == user_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e