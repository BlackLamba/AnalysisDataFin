from typing import Optional, List

from app.repositories import TransactionRepository
from app.schemas.transaction_schema import TransactionCreate, TransactionStatsByPeriod, TransactionStatsByCategory
import uuid
from datetime import datetime


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def get_expenses_by_period(
            self, user_id: str, period: str, date: Optional[datetime] = None
    ) -> TransactionStatsByPeriod:
        """Получить расходы за период"""
        result = await self.repository.get_expenses_by_period(user_id, period, date)
        return TransactionStatsByPeriod(**result)

    async def get_income_by_period(
            self, user_id: str, period: str, date: Optional[datetime] = None
    ) -> TransactionStatsByPeriod:
        """Получить доходы за период"""
        result = await self.repository.get_income_by_period(user_id, period, date)
        return TransactionStatsByPeriod(**result)

    async def get_expenses_by_category(
            self, user_id: str, period: str, date: Optional[datetime] = None
    ) -> List[TransactionStatsByCategory]:
        """Получить расходы по категориям"""
        results = await self.repository.get_expenses_by_category(user_id, period, date)
        return [TransactionStatsByCategory(**item) for item in results]

    async def get_income_by_category(
            self, user_id: str, period: str, date: Optional[datetime] = None
    ) -> List[TransactionStatsByCategory]:
        """Получить доходы по категориям"""
        results = await self.repository.get_income_by_category(user_id, period, date)
        return [TransactionStatsByCategory(**item) for item in results]