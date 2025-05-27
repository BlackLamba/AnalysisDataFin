from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.transactions import Transaction as TransactionModel
from app.schemas.transaction_schema import TransactionCreate
import uuid
from datetime import datetime


class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, transaction_data: TransactionCreate) -> TransactionModel:
        try:
            new_transaction = TransactionModel(
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

    async def get(self, transaction_id: str) -> TransactionModel | None:
        try:
            result = await self.db.execute(
                select(TransactionModel).where(TransactionModel.TransactionID == transaction_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e