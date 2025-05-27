from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum


class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50, alias="Name")
    type: CategoryType = Field(..., alias="Type")
    category: str = Field(..., max_length=50, alias="Category")  # Основная категория
    parent_id: Optional[UUID] = Field(None, alias="ParentID")


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