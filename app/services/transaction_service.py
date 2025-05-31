import statistics
from collections import Counter
from decimal import Decimal
from typing import Optional, List

from fastapi import HTTPException
from pydantic import UUID4

from app.repositories import TransactionRepository
from app.schemas.transaction_schema import (
    TransactionStatsByCategory,
    TransactionStats, TransactionReport, TransactionStatsByCategoryResponse, TransactionStatsResponse,
    TransactionReportResponse
)
import uuid
from datetime import datetime, timedelta


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def _get_period(self, period: str, date: Optional[datetime] = None
) -> str:
        # Вычисляем период для заголовка
        if period == "day":
            period_label = date.date().isoformat() if date else datetime.utcnow().date().isoformat()
        elif period == "week":
            start = date - timedelta(days=date.weekday())
            end = start + timedelta(days=6)
            period_label = f"{start.date()} – {end.date()}"
        elif period == "month":
            date = date or datetime.utcnow()
            period_label = f"{date.year}-{date.month:02d}"
        elif period == "year":
            date = date or datetime.utcnow()
            period_label = str(date.year)
        else:
            period_label = period
        return period_label

    async def get_stats_by_period(
            self,
            user_id: UUID4,
            period: str,
            date: Optional[datetime] = None
    ) -> TransactionStatsResponse:
        raw_data = await self.repository.get_stats_by_period(user_id, period, date)

        # Если репозиторий не возвращает "period", получаем его из даты
        if 'period' not in raw_data or raw_data['period'] is None:
            raw_data['period'] = self._get_period(period, date)

        return TransactionStatsResponse(**{
            "period": raw_data["period"],
            "data": raw_data["data"]
        })

    async def get_transactions_by_type_and_period(
            self,
            user_id: UUID4,
            type: str,
            period: str,
            date: Optional[datetime] = None
    ) -> TransactionStatsByCategoryResponse:
        results = await self.repository.get_type_by_category(user_id, type.upper(), period, date)
        period_label = self._get_period(period, date)

        return TransactionStatsByCategoryResponse(**{
            "period": period_label,
            "data": [TransactionStatsByCategory(**item) for item in results]
        })

    @staticmethod
    def calculate_stats(amounts: List[Decimal]) -> dict:
        """Рассчитывает статистику по списку сумм"""
        if not amounts:
            return {
                "total": 0.0,
                "average": 0.0,
                "median": 0.0,
                "mode": None
            }

        amounts = list(map(float, amounts))
        total = round(sum(amounts), 2)
        average = round(statistics.mean(amounts), 2)

        try:
            median = round(statistics.median(amounts), 2)
        except statistics.StatisticsError:
            median = 0.0

        try:
            mode = round(statistics.mode(amounts), 2)
        except statistics.StatisticsError:
            mode = None

        return {
            "total": total,
            "average": average,
            "median": median,
            "mode": mode
        }

    async def get_descriptive_stats_by_period(
            self,
            user_id: UUID4,
            period: str,
            date: Optional[datetime] = None
    ) -> TransactionReportResponse:
        """
        Получает данные за указанный период и возвращает описательную статистику
        """
        raw_data = await self.repository.get_stats_by_period(user_id, period, date)

        # Если репозиторий не вернул "period", строим его
        period_label = raw_data.get("period") or self._get_period(period, date)

        incomes = [item["total_amount"] for item in raw_data["data"] if item["category_type"] == "INCOME"]
        expenses = [item["total_amount"] for item in raw_data["data"] if item["category_type"] == "EXPENSE"]

        income_stats = TransactionService.calculate_stats(incomes)
        expense_stats = TransactionService.calculate_stats(expenses)

        return TransactionReportResponse(**{
            "period": period_label,
            "data": [
                TransactionReport(**{
                    "total_income": income_stats["total"],
                    "total_expense": expense_stats["total"],
                    "average_income": income_stats["average"],
                    "average_expense": expense_stats["average"],
                    "median_income": income_stats["median"],
                    "median_expense": expense_stats["median"],
                    "mode_income": income_stats["mode"],
                    "mode_expense": expense_stats["mode"]
                })
            ]
        })