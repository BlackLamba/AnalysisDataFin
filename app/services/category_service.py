from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, Category as CategorySchema
import uuid

from typing import List

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category_data: CategoryCreate) -> Category:
        try:
            new_category = Category(
                CategoryID=uuid.uuid4(),
                Type=category_data.type.value,
                Category=category_data.category
            )
            self.db.add(new_category)
            await self.db.commit()
            await self.db.refresh(new_category)
            return new_category
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, category_id: str) -> Category | None:
        try:
            result = await self.db.execute(
                select(Category).where(Category.CategoryID == category_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e

    async def get_all(self) -> List[CategorySchema]:
        try:
            result = await self.db.execute(select(Category))
            categories = result.scalars().all()
            return [CategorySchema.model_validate(cat) for cat in categories]
        except SQLAlchemyError as e:
            raise e