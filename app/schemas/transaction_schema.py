from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, UUID4, model_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date


class TransactionCreate(BaseModel):
    user_id: UUID4 = Field(..., alias="UserID")
    category_id: UUID4 = Field(..., alias="CategoryID")
    amount: float = Field(..., alias="Amount")
    account_id: UUID4 = Field(..., alias="AccountID")
    description: Optional[str] = Field(None, max_length=255, alias="Description")
    transaction_date: Optional[datetime] = Field(None, alias="TransactionDate")  # можно не передавать


class Transaction(TransactionCreate):
    transaction_id: UUID4 = Field(..., alias="TransactionID")

    model_config = ConfigDict(
        from_attributes=True
    )


class TransactionUpdate:
    pass


class TransactionStatsByHour(BaseModel):
    type: str = Field(..., alias="category_type")
    amount: float = Field(..., alias="total_amount")
    hour: int = Field(..., alias="transaction_hour")

    @model_validator(mode="before")
    @classmethod
    def convert_values(cls, values):
        # Создаем обычный dict, чтобы можно было изменять
        values = dict(values)  # <-- Вот ключевой момент!

        if isinstance(values.get("transaction_day"), date):
            values["transaction_day"] = values["transaction_day"].isoformat()

        if "transaction_hour" in values and isinstance(values["transaction_hour"], Decimal):
            values["transaction_hour"] = int(values["transaction_hour"])

        if "total_amount" in values and isinstance(values["total_amount"], (int, float, Decimal)):
            values["total_amount"] = float(values["total_amount"])

        return values

class TransactionStatsByDayWithHours(BaseModel):
    day: str
    data: List[TransactionStatsByHour]

class TransactionStatsByDay(BaseModel):
    type: str = Field(..., alias="category_type")
    amount: float = Field(..., alias="total_amount")
    day: str = Field(..., alias="transaction_day")

    @model_validator(mode="before")
    @classmethod
    def convert_values(cls, values):
        values = dict(values)

        if isinstance(values.get("transaction_day"), date):
            values["transaction_day"] = values["transaction_day"].isoformat()

        if "total_amount" in values and isinstance(values["total_amount"], (int, float, Decimal)):
            values["total_amount"] = float(values["total_amount"])

        return values


class TransactionStatsByWeek(BaseModel):
    week_range: str
    data: List[TransactionStatsByDay]


class TransactionStatsByDayInMonth(BaseModel):
    type: str = Field(..., alias="category_type")
    amount: float = Field(..., alias="total_amount")
    day: str = Field(..., alias="transaction_day")

    @model_validator(mode="before")
    @classmethod
    def convert_date_to_str(cls, values):
        values = dict(values)  # <- делаем копию, т.к. RowMapping неизменяемый
        if isinstance(values.get("transaction_day"), date):
            values["transaction_day"] = values["transaction_day"].isoformat()
        return values


class TransactionStatsByMonth(BaseModel):
    month: str
    data: List[TransactionStatsByDayInMonth]


class TransactionStatsByMonthInYear(BaseModel):
    type: str = Field(..., alias="category_type")
    amount: float = Field(..., alias="total_amount")
    month: str = Field(..., alias="transaction_month")

    @model_validator(mode="before")
    @classmethod
    def convert_values(cls, values):
        values = dict(values)

        if "total_amount" in values and isinstance(values["total_amount"], (int, float, Decimal)):
            values["total_amount"] = float(values["total_amount"])

        return values


class TransactionStatsByYear(BaseModel):
    year: str
    data: List[TransactionStatsByMonthInYear]


class TransactionStatsByCategory(BaseModel):
    category_name: str = Field(..., alias="category_name")
    total_amount: float = Field(..., alias="total_amount")
    count: int = Field(..., alias="count")

    model_config = ConfigDict(
        from_attributes=True
    )