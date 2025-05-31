from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    AccountID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.UserID"), nullable=False)
    AccountNumber = Column(String(50), nullable=False)
    BankName = Column(String(100))
    Currency = Column(String(3), server_default="RUB")
    Balance = Column(Numeric(15, 2), server_default="0")
    IsActive = Column(Boolean, server_default="true")

    # Relationships
    user = relationship("User", back_populates="accounts")
    recurring_payments = relationship("RecurringPayment", back_populates="account")

    __table_args__ = (
        UniqueConstraint("UserID", "AccountNumber", name="unique_user_account"),
    )