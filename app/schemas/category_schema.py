from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum


class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class CategoryBase(BaseModel):
    type: CategoryType = Field(..., alias="Type")
    category: str = Field(..., max_length=50, alias="Category")  # Основная категория


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    category_id: UUID = Field(..., alias="CategoryID")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class CategoryUpdate:
    pass