from typing import Optional

from pydantic import BaseModel, Field
from datetime import date
from app.schemas.base_schema import BaseSchema, IDSchema

class SavingsGoalBase(BaseSchema):
    name: str = Field(..., max_length=100)
    target_amount: float = Field(..., gt=0)
    target_date: Optional[date] = None
    description: Optional[str] = None

class SavingsGoalCreate(SavingsGoalBase):
    user_id: str

class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    target_amount: Optional[float] = Field(None, gt=0)
    target_date: Optional[date] = None
    description: Optional[str] = None

class SavingsGoal(IDSchema, SavingsGoalBase):
    current_amount: float = Field(default=0)
    user_id: str