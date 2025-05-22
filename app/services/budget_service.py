from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.budget import Budget as BudgetModel
from app.schemas.budget_schema import BudgetCreate
import uuid


class BudgetService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, budget_data: BudgetCreate) -> BudgetModel:
        try:
            new_budget = BudgetModel(
                BudgetID=uuid.uuid4(),
                UserID=budget_data.user_id,
                CategoryID=budget_data.category_id,
                Amount=budget_data.amount,
                Period=budget_data.period,
                StartDate=budget_data.date,
                EndDate=budget_data.date,
            )
            self.db.add(new_budget)
            await self.db.commit()
            await self.db.refresh(new_budget)
            return new_budget
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, budget_id: str) -> BudgetModel | None:
        try:
            result = await self.db.execute(
                select(BudgetModel).where(BudgetModel.BudgetID == budget_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e