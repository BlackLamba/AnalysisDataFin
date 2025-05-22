from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class SavingsGoalCreate(BaseModel):
    user_id: UUID
    name: str = Field(..., max_length=100)
    target_amount: float
    target_date: Optional[datetime] = None
    description: Optional[str] = Field(None, max_length=255)


class SavingsGoal(SavingsGoalCreate):
    id: UUID
    current_amount: float

    model_config = ConfigDict(
        from_attributes=True
    )