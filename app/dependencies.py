from app.repositories.transaction_repository import TransactionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db

def get_transaction_repo(db: AsyncSession = Depends(get_db)) -> TransactionRepository:
    return TransactionRepository(db)