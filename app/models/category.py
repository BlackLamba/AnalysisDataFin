from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum
import uuid

class CategoryType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Base):
    __tablename__ = "categories"

    CategoryID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ParentID = Column(UUID(as_uuid=True), ForeignKey("categories.CategoryID"))
    Name = Column(String(50), nullable=False)
    Type = Column(Enum(CategoryType, name="category_type_enum", inherit_schema=True), nullable=False)
    Category = Column(String(50), nullable=False)  # Основная категория

    # Relationships
    parent = relationship("Category", remote_side=[CategoryID], foreign_keys=[ParentID], back_populates="children")
    children = relationship("Category", back_populates="parent")

    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")
    recurring_payments = relationship("RecurringPayment", back_populates="category")