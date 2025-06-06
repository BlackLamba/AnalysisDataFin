from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func


class Transaction(Base):
    __tablename__ = "transactions"

    TransactionID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.UserID"), nullable=False)
    AccountID = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.AccountID"), nullable=False, index=True)
    CategoryID = Column(UUID(as_uuid=True), ForeignKey("categories.CategoryID"), nullable=False, index=True)
    Amount = Column(Numeric(15, 2), nullable=False)
    Description = Column(String(255))
    TransactionDate = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    account = relationship("BankAccount", back_populates="transactions")