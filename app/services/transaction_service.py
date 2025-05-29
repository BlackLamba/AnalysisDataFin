from typing import Optional, List

from app.repositories import TransactionRepository
from app.schemas.transaction_schema import TransactionStatsByCategory, \
    TransactionStatsByHour, TransactionStatsByDay, TransactionStatsByWeek, TransactionStatsByMonth, \
    TransactionStatsByYear
import uuid
from datetime import datetime


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def get_stats_by_hour(
            self,
            user_id: str,
            date: Optional[datetime] = None
    ) -> List[TransactionStatsByHour]:
        """
        Получает агрегированные данные по транзакциям за день, сгруппированные по часам и типу
        """
        data = await self.repository.get_stats_by_hour(user_id, date)
        return [TransactionStatsByHour(**item) for item in data]

    async def get_income_by_hour(
            self,
            user_id: str,
            date: Optional[datetime] = None
    ) -> List[TransactionStatsByHour]:
        """
        Получает только доходы за день, сгруппированные по часам
        """
        all_data = await self.get_stats_by_hour(user_id, date)
        return [item for item in all_data if item.type == "INCOME"]

    async def get_expenses_by_hour(
            self,
            user_id: str,
            date: Optional[datetime] = None
    ) -> List[TransactionStatsByHour]:
        """
        Получает только расходы за день, сгруппированные по часам
        """
        all_data = await self.get_stats_by_hour(user_id, date)
        return [item for item in all_data if item.type == "EXPENSE"]

    async def get_stats_by_week(
            self,
            user_id: str,
            date: Optional[datetime] = None
    ) -> TransactionStatsByWeek:
        raw_data = await self.repository.get_stats_by_week(user_id, date)
        return TransactionStatsByWeek(**raw_data)

    async def get_stats_by_month(
            self,
            user_id: str,
            date: Optional[datetime] = None
    ) -> TransactionStatsByMonth:
        raw_data = await self.repository.get_stats_by_month(user_id, date)
        return TransactionStatsByMonth(**raw_data)

    async def get_stats_by_year(
            self,
            user_id: str,
            date: Optional[datetime] = None
    ) -> TransactionStatsByYear:
        raw_data = await self.repository.get_stats_by_year(user_id, date)
        return TransactionStatsByYear(**raw_data)

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