from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.savings_goal import SavingsGoal as SavingsGoalModel
from app.schemas.savings_goal_schema import SavingsGoalCreate
import uuid


class SavingsGoalService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, goal_data: SavingsGoalCreate) -> SavingsGoalModel:
        try:
            new_goal = SavingsGoalModel(
                id=uuid.uuid4(),
                UserID=goal_data.user_id,
                Name=goal_data.name,
                TargetAmount=goal_data.target_amount,
                TargetDate=goal_data.target_date,
                Description=goal_data.description,
                CurrentAmount=0.00  # начальное значение
            )
            self.db.add(new_goal)
            await self.db.commit()
            await self.db.refresh(new_goal)
            return new_goal
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, goal_id: str) -> SavingsGoalModel | None:
        try:
            result = await self.db.execute(
                select(SavingsGoalModel).where(SavingsGoalModel.id == goal_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e