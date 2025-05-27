from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional
from uuid import UUID
from datetime import datetime


class SavingsGoalCreate(BaseModel):
    user_id: UUID4 = Field(..., alias="UserID")
    name: str = Field(..., max_length=100, alias="Name")
    target_amount: float = Field(..., alias="TargetAmount")
    target_date: Optional[datetime] = Field(None, alias="TargetDate")
    description: Optional[str] = Field(None, max_length=255, alias="Description")
    current_amount: float = Field(..., alias="CurrentAmount")


class SavingsGoal(SavingsGoalCreate):
    id: UUID4 = Field(..., alias="id")
    current_amount: float

    model_config = ConfigDict(
        from_attributes=True
    )