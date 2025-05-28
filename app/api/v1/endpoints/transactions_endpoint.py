from datetime import datetime
from typing import Optional, List

from fastapi import Depends, HTTPException, Query, Path
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction_schema import (
    TransactionCreate,
    Transaction,
    TransactionStatsByPeriod,
    TransactionStatsByCategory
)
from app.repositories.transaction_repository import TransactionRepository
from app.dependencies import get_transaction_repo
from .deps import get_current_user_id
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/transactions", tags=["transactions"]).router


@router.post("", response_model=Transaction, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate,
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    return await repo.create(transaction_data)


@router.get("/{transaction_id}", response_model=Transaction)
async def read_transaction(
    transaction_id: UUID4,
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    transaction = await repo.get_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/stats/period/{period}", response_model=TransactionStatsByPeriod)
async def get_period_stats(
    period: str = Path(..., regex="^(day|week|month|year)$"),
    date: Optional[datetime] = None,
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    result = await repo.get_expenses_by_period(user_id, period, date)
    return TransactionStatsByPeriod(**result)


@router.get("/expenses/categories/{period}", response_model=List[TransactionStatsByCategory])
async def get_expenses_by_category(
    period: str = Path(..., regex="^(day|week|month|year)$"),
    date: Optional[datetime] = None,
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    data = await repo.get_expenses_by_category(user_id, period, date)
    return [TransactionStatsByCategory(**item) for item in data]


@router.get("/income/categories/{period}", response_model=List[TransactionStatsByCategory])
async def get_income_by_category(
    period: str = Path(..., regex="^(day|week|month|year)$"),
    date: Optional[datetime] = None,
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    data = await repo.get_income_by_category(user_id, period, date)
    return [TransactionStatsByCategory(**item) for item in data]