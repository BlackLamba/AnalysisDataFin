from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, UUID4, model_validator
from typing import Optional, List, Union
from uuid import UUID
from datetime import datetime, date


class TransactionCreate(BaseModel):
    user_id: UUID4 = Field(..., alias="UserID")
    category_id: UUID4 = Field(..., alias="CategoryID")
    amount: float = Field(..., alias="Amount")
    account_id: Optional[UUID4] = Field(None, alias="AccountID")
    description: Optional[str] = Field(None, max_length=255, alias="Description")
    transaction_date: Optional[datetime] = Field(None, alias="TransactionDate")  # можно не передавать


class Transaction(TransactionCreate):
    transaction_id: UUID4 = Field(..., alias="TransactionID")

    model_config = ConfigDict(
        from_attributes=True
    )


class TransactionStats(BaseModel):
    type: str = Field(..., alias="category_type")
    amount: float = Field(..., alias="total_amount")
    period: Union[int, str] = Field(..., alias="transaction_period")  # может быть днём, месяцем, годом, часом

    @model_validator(mode="before")
    def convert_values(cls, values):
        values = dict(values)

        if "total_amount" in values and isinstance(values["total_amount"], (int, float, Decimal)):
            values["total_amount"] = float(values["total_amount"])

        if "transaction_hour" in values:
            values["transaction_period"] = int(values["transaction_hour"])
        elif "transaction_day" in values:
            if isinstance(values["transaction_day"], date):
                values["transaction_period"] = values["transaction_day"].isoformat()
            else:
                values["transaction_period"] = values["transaction_day"]
        elif "transaction_month" in values:
            values["transaction_period"] = values["transaction_month"]

        return values


class TransactionStatsResponse(BaseModel):
    period: str
    data: List[TransactionStats]


class TransactionReport(BaseModel):
    total_income: float
    total_expense: float
    average_income: float
    average_expense: float
    median_income: float
    median_expense: float
    mode_income: Optional[float] = None
    mode_expense: Optional[float] = None

    @model_validator(mode="before")
    @classmethod
    def convert_values(cls, values):
        values = dict(values)

        if "total_amount" in values and isinstance(values["total_amount"], (int, float, Decimal)):
            values["total_amount"] = float(values["total_amount"])

        if "transaction_hour" in values:
            values["transaction_period"] = int(values["transaction_hour"])
        elif "transaction_day" in values:
            if isinstance(values["transaction_day"], date):
                values["transaction_period"] = values["transaction_day"].isoformat()
            else:
                values["transaction_period"] = values["transaction_day"]
        elif "transaction_month" in values:
            values["transaction_period"] = values["transaction_month"]

        return values


class TransactionReportResponse(BaseModel):
    period: str
    data: List[TransactionReport]


class TransactionStatsByCategory(BaseModel):
    category_name: str = Field(..., alias="category_name")
    total_amount: float = Field(..., alias="total_amount")
    count: int = Field(..., alias="count")

    @model_validator(mode="before")
    @classmethod
    def convert_values(cls, values):
        values = dict(values)

        if "total_amount" in values and isinstance(values["total_amount"], (int, float, Decimal)):
            values["total_amount"] = float(values["total_amount"])

        if "transaction_day" in values and isinstance(values["transaction_day"], datetime):
            values["transaction_period"] = values["transaction_day"].isoformat()
        elif "transaction_hour" in values:
            values["transaction_period"] = int(values["transaction_hour"])
        elif "transaction_month" in values:
            values["transaction_period"] = values["transaction_month"]
        elif "transaction_year" in values:
            values["transaction_period"] = values["transaction_year"]

        return values

    model_config = ConfigDict(from_attributes=True)


class TransactionStatsByCategoryResponse(BaseModel):
    period: str
    data: List[TransactionStatsByCategory]