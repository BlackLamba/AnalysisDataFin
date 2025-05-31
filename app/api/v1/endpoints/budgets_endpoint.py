from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.budget_schema import BudgetCreate, Budget
from app.services.budget_service import BudgetService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/budgets", tags=["budgets"]).router

@router.post("", response_model=Budget, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    db: AsyncSession = Depends(get_db)
):
    service = BudgetService(db)
    return await service.create(budget_data=budget_data)

@router.get("/{budget_id}", response_model=Budget)
async def read_budget(
    budget_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = BudgetService(db)
    budget = await service.get(budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget