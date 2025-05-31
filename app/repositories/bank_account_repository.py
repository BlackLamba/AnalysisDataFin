from app.models.bank_account import BankAccount
from app.repositories.base_repository import BaseRepository
from app.schemas.bank_account_schema import BankAccountCreate, BankAccountUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, UUID
from typing import List

class BankAccountRepository(BaseRepository[BankAccount, BankAccountCreate, BankAccountUpdate]):
    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[BankAccount]:
        result = await db.execute(
            select(BankAccount)
            .where(BankAccount.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update_balance(
        self,
        db: AsyncSession,
        *,
        account_id: UUID,
        amount: float
    ) -> BankAccount:
        account = await self.get(db, id=account_id)
        if account:
            account.balance += amount
            db.add(account)
            await db.commit()
            await db.refresh(account)
        return account