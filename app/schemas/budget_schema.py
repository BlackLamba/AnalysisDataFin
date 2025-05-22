from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class BudgetBase(BaseModel):
    user_id: str = Field(..., alias="UserID")
    category_id: str = Field(..., alias="CategoryID")
    amount: float = Field(..., alias="Amount")
    period: str = Field(..., alias="Period")  # "day", "week", "month", "year"
    start_date: datetime = Field(..., alias="StartDate")
    end_date: Optional[datetime] = Field(None, alias="EndDate")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    budget_id: str = Field(..., alias="BudgetID")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )