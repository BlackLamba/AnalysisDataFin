from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.user import User as UserModel
from app.schemas.user_schema import UserCreate
import uuid


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate) -> UserModel:
        try:
            new_user = UserModel(
                UserID=uuid.uuid4(),
                LastName=user_data.last_name,
                FirstName=user_data.first_name,
                MiddleName=user_data.middle_name,
                PassportNumber=user_data.passport_number,
                Email=user_data.email,
                hashed_password=user_data.hashed_password
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("User with this email already exists.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, user_id: str) -> UserModel | None:
        try:
            result = await self.db.execute(
                select(UserModel).where(UserModel.UserID == user_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e