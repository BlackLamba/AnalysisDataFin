from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.savings_goal_schema import SavingsGoalCreate, SavingsGoalOut
from app.services.savings_goal_service import SavingsGoalService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/goals", tags=["goals"]).router

@router.post("/", response_model=SavingsGoalOut, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: SavingsGoalCreate,
    db: AsyncSession = Depends(get_db)
):
    service = SavingsGoalService(db)
    return await service.create(goal_data=goal_data)

@router.get("/{goal_id}", response_model=SavingsGoalOut)
async def read_goal(
    goal_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = SavingsGoalService(db)
    goal = await service.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal