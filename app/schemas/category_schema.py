from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base_schema import BaseSchema, IDSchema

class CategoryBase(BaseSchema):
    name: str = Field(..., max_length=50)
    type: str = Field(..., regex="^(income|expense)$")
    category: str = Field(..., max_length=50)  # Основная категория
    parent_id: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    type: Optional[str] = Field(None, regex="^(income|expense)$")

class Category(IDSchema, CategoryBase):
    pass