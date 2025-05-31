from app.repositories.transaction_repository import TransactionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from fastapi import Depends
from typing import Annotated

from .repositories import TransactionRepository
from .services import TransactionService

def get_transaction_repo(db: AsyncSession = Depends(get_db)) -> TransactionRepository:
    return TransactionRepository(db)

async def get_transaction_service(
    repo: Annotated[TransactionRepository, Depends(get_transaction_repo)]
) -> TransactionService:
    return TransactionService(repository=repo)