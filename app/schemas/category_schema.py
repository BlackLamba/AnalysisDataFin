from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    type: CategoryType
    category: str = Field(..., max_length=50)  # Основная категория
    parent_id: Optional[UUID] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    category_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class CategoryUpdate:
    pass