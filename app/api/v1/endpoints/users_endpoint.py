from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, User
from app.services.user_service import UserService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/users", tags=["users"]).router

@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.create(user_data=user_data)

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user