import uuid

from pydantic import UUID4
from sqlalchemy import select, func, and_, extract, RowMapping, Integer, cast
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from typing import List, Optional, Any, Mapping, Sequence, Dict
from app.models import Transaction, Category
from app.schemas import transaction_schema, TransactionCreate

from typing import List, Tuple
from sqlalchemy.sql.elements import BinaryExpression


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _get_period_filters(
            self,
            date_column,
            period: str,
            date: datetime
    ) -> List[BinaryExpression]:
        """Генерирует фильтры для временного периода"""
        filters = []

        if period == 'day':
            filters.append(func.date(date_column) == date.date())
        elif period == 'week':
            start = date - timedelta(days=date.weekday())
            end = start + timedelta(days=6)
            filters.extend([
                func.date(date_column) >= start.date(),
                func.date(date_column) <= end.date()
            ])
        elif period == 'month':
            filters.extend([
                extract('month', date_column) == date.month,
                extract('year', date_column) == date.year
            ])
        elif period == 'year':
            filters.append(extract('year', date_column) == date.year)
        else:
            raise ValueError(f"Unknown period: {period}")

        return filters

    async def _get_aggregated_data(
            self,
            user_id: str,
            category_type: str,  # Например: 'INCOME' или 'EXPENSE'
            period: str = 'month',
            date: Optional[datetime] = None,
            group_by_column=None
    ) -> list[Mapping[Any, Any]] | Sequence[RowMapping]:
        """Базовый метод для агрегации данных по типу категории"""
        date = date or datetime.utcnow()

        filters = [
            Transaction.UserID == user_id,
            Category.Type == category_type  # Фильтруем транзакции по типу категории
        ]

        # Добавляем фильтры по периоду
        filters.extend(self._get_period_filters(Transaction.TransactionDate, period, date))

        query = select(
            func.sum(Transaction.Amount).label("total_amount"),
            func.count().label("count")
        ).join(Category, Transaction.CategoryID == Category.CategoryID) \
            .where(and_(*filters))

        if group_by_column is not None:
            query = query.add_columns(group_by_column).group_by(group_by_column)

        result = await self.db.execute(query)
        return result.mappings().all()

    # Обновленные методы

    async def get_expenses_by_category(self, user_id: UUID4, period: str, date: Optional[datetime] = None) -> List[
        dict]:
        return await self._get_aggregated_data(
            user_id=user_id,
            category_type='EXPENSE',  # Фильтруем только доходы
            period=period,
            date=date,
            group_by_column=Category.Category.label("category_name")
        )

    async def get_income_by_category(self, user_id: UUID4, period: str, date: Optional[datetime] = None) -> List[
        dict]:
        return await self._get_aggregated_data(
            user_id=user_id,
            category_type='INCOME',  # Фильтруем только доходы
            period=period,
            date=date,
            group_by_column=Category.Category.label("category_name")
        )

    async def get_stats_by_day_with_hours(self, user_id: UUID4, date: Optional[datetime] = None) -> dict:
        """
        Получить агрегированные данные по транзакциям за день, сгруппированные по часам и типу категории
        """
        date = date or datetime.utcnow()

        query = (
            select(
                Category.Type.label("category_type"),
                func.sum(func.abs(Transaction.Amount)).label("total_amount"),
                cast(extract('hour', Transaction.TransactionDate), Integer).label("transaction_hour")
            )
            .join(Category, Transaction.CategoryID == Category.CategoryID)
            .where(
                Transaction.UserID == user_id,
                func.date(Transaction.TransactionDate) == date.date()
            )
            .group_by(
                Category.Type,
                extract('hour', Transaction.TransactionDate)
            )
            .order_by(extract('hour', Transaction.TransactionDate))
        )

        result = await self.db.execute(query)
        rows = result.mappings().all()

        return {
            "day": date.date().isoformat(),
            "data": rows
        }

    async def get_stats_by_week(self, user_id: UUID4, date: Optional[datetime] = None) -> dict:
        """
        Получить агрегированные данные по транзакциям за неделю
        """
        date = date or datetime.utcnow()

        # Начало недели (понедельник)
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        query = (
            select(
                Category.Type.label("category_type"),
                func.sum(func.abs(Transaction.Amount)).label("total_amount"),
                func.date(Transaction.TransactionDate).label("transaction_day")
            )
            .join(Category, Transaction.CategoryID == Category.CategoryID)
            .where(
                Transaction.UserID == user_id,
                func.date(Transaction.TransactionDate).between(
                    start_of_week.date(),
                    end_of_week.date()
                )
            )
            .group_by(
                Category.Type,
                func.date(Transaction.TransactionDate)
            )
            .order_by(func.date(Transaction.TransactionDate))
        )

        result = await self.db.execute(query)
        rows = result.mappings().all()

        return {
            "week_range": f"{start_of_week.date()} – {end_of_week.date()}",
            "data": rows
        }

    async def get_stats_by_month(self, user_id: UUID4, date: Optional[datetime] = None) -> dict:
        date = date or datetime.utcnow()

        query = (
            select(
                Category.Type.label("category_type"),
                func.sum(func.abs(Transaction.Amount)).label("total_amount"),
                func.date(Transaction.TransactionDate).label("transaction_day")
            )
            .join(Category, Transaction.CategoryID == Category.CategoryID)
            .where(
                Transaction.UserID == user_id,
                extract('year', Transaction.TransactionDate) == date.year,
                extract('month', Transaction.TransactionDate) == date.month
            )
            .group_by(
                Category.Type,
                func.date(Transaction.TransactionDate)
            )
            .order_by(func.date(Transaction.TransactionDate))
        )

        result = await self.db.execute(query)
        rows = result.mappings().all()

        # Преобразуем даты в строки
        cleaned_data = [
            {
                "category_type": row["category_type"],
                "total_amount": float(row["total_amount"]),
                "transaction_day": row["transaction_day"].isoformat()  # <-- date → str
            }
            for row in rows
        ]

        return {
            "month": f"{date.year}-{date.month:02d}",
            "data": cleaned_data
        }

    from sqlalchemy import func, select, text
    from app.models import Transaction, Category

    async def get_stats_by_year(self, user_id: UUID4, date: Optional[datetime] = None) -> dict:
        date = date or datetime.utcnow()

        transaction_month = func.to_char(Transaction.TransactionDate, 'YYYY-MM').label("transaction_month")

        query = (
            select(
                Category.Type.label("category_type"),
                func.sum(func.abs(Transaction.Amount)).label("total_amount"),
                transaction_month
            )
            .join(Category, Transaction.CategoryID == Category.CategoryID)
            .where(
                Transaction.UserID == str(user_id),
                extract('year', Transaction.TransactionDate) == date.year
            )
            .group_by(
                Category.Type,
                transaction_month
            )
            .order_by(transaction_month)
        )

        result = await self.db.execute(query)
        rows = result.mappings().all()

        # Убедимся, что возвращается поле `year`, а не `month`
        return {
            "year": str(date.year),  # <-- Вот он ключевой момент!
            "data": [
                {
                    "category_type": row["category_type"],
                    "total_amount": float(row["total_amount"]),
                    "transaction_month": row["transaction_month"]
                }
                for row in rows
            ]
        }

    async def create(self, transaction_data: TransactionCreate) -> Transaction:
        try:
            new_transaction = Transaction(
                TransactionID=uuid.uuid4(),
                UserID=transaction_data.user_id,
                CategoryID=transaction_data.category_id,
                AccountID=transaction_data.account_id,
                Amount=transaction_data.amount,
                Description=transaction_data.description,
                TransactionDate=transaction_data.transaction_date or datetime.utcnow(),
            )
            self.db.add(new_transaction)
            await self.db.commit()
            await self.db.refresh(new_transaction)
            return new_transaction
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get_by_id(self, transaction_id: uuid.UUID) -> Optional[Transaction]:
        try:
            result = await self.db.execute(
                select(Transaction).where(Transaction.TransactionID == transaction_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e