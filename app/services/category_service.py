from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.category import Category as CategoryModel
from app.schemas.category_schema import CategoryCreate
import uuid


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category_data: CategoryCreate) -> CategoryModel:
        try:
            new_category = CategoryModel(
                CategoryID=uuid.uuid4(),
                ParentID=category_data.parent_id,
                Name=category_data.name,
                type=category_data.type,
                Category=category_data.category
            )
            self.db.add(new_category)
            await self.db.commit()
            await self.db.refresh(new_category)
            return new_category
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, category_id: str) -> CategoryModel | None:
        try:
            result = await self.db.execute(
                select(CategoryModel).where(CategoryModel.CategoryID == category_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e