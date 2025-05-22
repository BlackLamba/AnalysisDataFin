from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy import ForeignKeyConstraint, CheckConstraint
from app.models.base import Base


class RecurringPayment(Base):
    __tablename__ = "recurring_payments"

    PaymentID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, nullable=False)
    CategoryID = Column(Integer)
    AccountID = Column(Integer)
    Name = Column(String(100), nullable=False)
    Amount = Column(Numeric(15, 2), nullable=False)
    Frequency = Column(String(8), nullable=False)
    StartDate = Column(DateTime, nullable=False)
    EndDate = Column(DateTime)

    __table_args__ = (
        ForeignKeyConstraint(['UserID'], ['users.UserID'], ondelete='CASCADE'),
        ForeignKeyConstraint(['CategoryID'], ['categories.CategoryID'], ondelete='SET NULL'),
        ForeignKeyConstraint(['AccountID'], ['bank_accounts.AccountID'], ondelete='SET NULL'),
        CheckConstraint("Frequency IN ('daily', 'weekly', 'monthly', 'yearly')", name='check_frequency')
    )