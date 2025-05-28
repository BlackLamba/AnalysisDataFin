import uuid

from pydantic import UUID4
from sqlalchemy import select, func, and_, extract, RowMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from typing import List, Optional, Any, Mapping, Sequence
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

    async def get_income_by_period(self, user_id: UUID4, period: str, date: Optional[datetime] = None) -> dict:
        data = await self._get_aggregated_data(
            user_id=user_id,
            period=period,
            date=date,
            category_type='INCOME'
        )
        if not data:
            return {"total_amount": 0.0, "count": 0}

        row = dict(data[0])
        return {
            "total_amount": float(row["total_amount"]) if row["total_amount"] is not None else 0.0,
            "count": row["count"]
        }

    async def get_expenses_by_period(self, user_id: UUID4, period: str, date: Optional[datetime] = None) -> dict:
        data = await self._get_aggregated_data(
            user_id=user_id,
            period=period,
            date=date,
            category_type='EXPENSE'
        )
        if not data:
            return {"total_amount": 0.0, "count": 0}

        row = dict(data[0])
        return {
            "total_amount": float(row["total_amount"]) if row["total_amount"] is not None else 0.0,
            "count": row["count"]
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