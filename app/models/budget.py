from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid


class Budget(Base):
    __tablename__ = "budgets"

    BudgetID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    CategoryID = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    Amount = Column(Numeric(15, 2), nullable=False)
    Period = Column(String(5), nullable=False)  # day, week, month, year
    StartDate = Column(DateTime, nullable=False)
    EndDate = Column(DateTime)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")