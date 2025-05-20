from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

class UserService(BaseService):
    def __init__(self, db: AsyncSession):
        super().__init__(UserRepository(User, db))

    async def create(self, *, obj_in: UserCreate):
        # Хешируем пароль перед созданием
        hashed_password = get_password_hash(obj_in.password)
        user_data = obj_in.model_dump(exclude={"password"})
        return await super().create(obj_in={**user_data, "hashed_password": hashed_password})

    async def authenticate(self, *, email: str, password: str):
        return await self.repository.authenticate(email=email, password=password)

    async def get_by_email(self, *, email: str):
        return await self.repository.get_by_email(email=email)