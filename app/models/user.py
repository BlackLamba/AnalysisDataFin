from sqlalchemy import Column, Enum, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base
import uuid


class User(Base):
    __tablename__ = "users"

    UserID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    LastName = Column(String(50), nullable=False)
    FirstName = Column(String(50), nullable=False)
    MiddleName = Column(String(50))
    PassportNumber = Column(String(20))
    Email = Column(String(100), unique=True)
    RegistrationDate = Column(DateTime, server_default="now()")
    hashed_password = Column(String(255), nullable=False)

    # Relationships
    accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    savings_goals = relationship("SavingsGoal", back_populates="user")
    recurring_payments = relationship("RecurringPayment", back_populates="user")