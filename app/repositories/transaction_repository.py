from app.models.transactions import Transaction
from app.repositories.base_repository import BaseRepository
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, UUID
from datetime import date
from typing import List, Optional


class TransactionRepository(BaseRepository[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_multi_by_user(
            self,
            db: AsyncSession,
            user_id: UUID,
            *,
            skip: int = 0,
            limit: int = 100,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> List[Transaction]:
        query = select(Transaction).where(Transaction.user_id == user_id)

        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_category(
            self,
            db: AsyncSession,
            category_id: UUID,
            *,
            skip: int = 0,
            limit: int = 100
    ) -> List[Transaction]:
        result = await db.execute(
            select(Transaction)
            .where(Transaction.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()