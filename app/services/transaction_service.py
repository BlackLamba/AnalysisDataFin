from app.models import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.services.base_service import BaseService
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional

class TransactionService(BaseService):
    def __init__(self, db: AsyncSession):
        super().__init__(TransactionRepository(Transaction, db))

    async def get_multi_by_user(
        self,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ):
        return await self.repository.get_multi_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date
        )

    async def get_by_category(self, *, category_id: int, skip: int = 0, limit: int = 100):
        return await self.repository.get_by_category(
            category_id=category_id,
            skip=skip,
            limit=limit
        )