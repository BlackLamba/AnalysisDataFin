from sqlalchemy import select

from app.core.security import verify_password
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def authenticate(
        self,
        db: AsyncSession,
        *,
        email: str,
        password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user