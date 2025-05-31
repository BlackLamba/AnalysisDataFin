import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy import ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base import Base

class FrequencyEnum(str, PyEnum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class RecurringPayment(Base):
    __tablename__ = "recurring_payments"

    PaymentID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.UserID"), nullable=False, index=True)
    CategoryID = Column(UUID(as_uuid=True), ForeignKey("categories.CategoryID"), nullable=False, index=True)
    AccountID = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.AccountID"), nullable=False, index=True)
    Name = Column(String(100), nullable=False)
    Amount = Column(Numeric(15, 2), nullable=False)
    Frequency = Column(
        Enum(FrequencyEnum, name="frequency_enum", create_constraint=True),
        nullable=False
    )
    StartDate = Column(DateTime, nullable=False)
    EndDate = Column(DateTime)

    user = relationship("User", back_populates="recurring_payments")
    category = relationship("Category", back_populates="recurring_payments")
    account = relationship("BankAccount", back_populates="recurring_payments")

    __table_args__ = (
        ForeignKeyConstraint(['CategoryID'], ['categories.CategoryID'], ondelete='SET NULL'),
        ForeignKeyConstraint(['AccountID'], ['bank_accounts.AccountID'], ondelete='SET NULL'),
        CheckConstraint(Frequency.in_(['daily', 'weekly', 'monthly', 'yearly']), name='check_frequency')
    )