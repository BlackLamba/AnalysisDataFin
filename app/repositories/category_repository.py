from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.base_repository import BaseRepository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from sqlalchemy import select, and_, UUID
from typing import List

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_type(
        self,
        db: AsyncSession,
        type: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.type == type)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_children(
        self,
        db: AsyncSession,
        parent_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.parent_id == parent_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()