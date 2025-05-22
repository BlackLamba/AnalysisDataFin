from sqlalchemy import Column, String, Numeric, Boolean, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid



class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    Name = Column(String(100), nullable=False)
    TargetAmount = Column(Numeric(15, 2), nullable=False)
    CurrentAmount = Column(Numeric(15, 2), server_default="0")
    TargetDate = Column(DateTime)
    Description = Column(String(255))

    user = relationship("User", back_populates="savings_goals")