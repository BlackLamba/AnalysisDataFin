from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category_schema import CategoryCreate, Category
from app.services.category_service import CategoryService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/categories", tags=["categories"]).router

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(db)
    return await service.create(category_data=category_data)

@router.get("/{category_id}", response_model=Category)
async def read_category(
    category_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(db)
    category = await service.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category