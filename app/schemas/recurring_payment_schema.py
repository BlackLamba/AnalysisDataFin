from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum


class FrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class RecurringPaymentCreate(BaseModel):
    user_id: UUID4 = Field(..., alias="UserID")
    category_id: UUID4 = Field(..., alias="CategoryID")
    account_id: UUID4 = Field(..., alias="AccountID")
    name: str = Field(..., max_length=100, alias="Name")
    amount: float = Field(..., alias="Amount")
    frequency: FrequencyEnum = Field(..., alias="Frequency")
    start_date: datetime = Field(..., alias="StartDate")
    end_date: Optional[datetime] = Field(None, alias="EndDate")


class RecurringPayment(RecurringPaymentCreate):
    payment_id: UUID4 = Field(..., alias="PaymentID")

    model_config = ConfigDict(
        from_attributes=True
    )