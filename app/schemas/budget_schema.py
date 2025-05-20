from typing import Optional

from pydantic import BaseModel, Field
from datetime import date
from app.schemas.base_schema import BaseSchema, IDSchema

class BudgetBase(BaseSchema):
    amount: float = Field(..., gt=0)
    period: str = Field(..., regex="^(day|week|month|year)$")
    start_date: date
    end_date: Optional[date] = None

class BudgetCreate(BudgetBase):
    user_id: str
    category_id: str

class BudgetUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    period: Optional[str] = Field(None, regex="^(day|week|month|year)$")
    end_date: Optional[date] = None

class Budget(IDSchema, BudgetBase):
    user_id: str
    category_id: str