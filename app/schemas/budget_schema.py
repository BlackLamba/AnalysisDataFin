from pydantic import BaseModel, Field, ConfigDict, UUID4
from datetime import datetime
from typing import Optional


class BudgetBase(BaseModel):
    user_id: UUID4 = Field(..., alias="UserID")  # И здесь тоже
    category_id: UUID4 = Field(..., alias="CategoryID")  # И здесь
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
    budget_id: UUID4 = Field(..., alias="BudgetID")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )