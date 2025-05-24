import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy import ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base


class RecurringPayment(Base):
    __tablename__ = "recurring_payments"

    PaymentID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.UserID"), nullable=False, index=True)
    CategoryID = Column(UUID(as_uuid=True), ForeignKey("categories.CategoryID"), nullable=False, index=True)
    AccountID = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.AccountID"), nullable=False, index=True)
    Name = Column(String(100), nullable=False)
    Amount = Column(Numeric(15, 2), nullable=False)
    Frequency = Column(String(8), nullable=False)
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