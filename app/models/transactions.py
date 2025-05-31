from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Transaction(Base):
    __tablename__ = "transactions"

    TransactionID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.UserID"), nullable=False)
    CategoryID = Column(UUID(as_uuid=True), ForeignKey("categories.CategoryID"), nullable=False, index=True)
    Amount = Column(Numeric(15, 2), nullable=False)
    Description = Column(String(255))
    TransactionDate = Column(DateTime, server_default="now()")

    # Связи
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")