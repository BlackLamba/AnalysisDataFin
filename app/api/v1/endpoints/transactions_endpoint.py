from datetime import datetime
from typing import Optional, List

from fastapi import Depends, HTTPException, Query, Path
from pydantic import UUID4
from app.schemas.transaction_schema import (
    TransactionCreate, Transaction, TransactionReportResponse,
    TransactionStatsResponse, TransactionStatsByCategoryResponse
)
from app.repositories.transaction_repository import TransactionRepository
from app.dependencies import get_transaction_repo
from .deps import get_current_user_id
from .base_endpoint import BaseRouter
from app.services.transaction_service import TransactionService

router = BaseRouter(prefix="/transactions", tags=["transactions"]).router


@router.post("", response_model=Transaction, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate,
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    return await repo.create(user_id, transaction_data)


@router.get("/{transaction_id}", response_model=Transaction)
async def read_transaction(
    transaction_id: UUID4,
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    transaction = await repo.get_by_id(user_id, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/stats/{period}", response_model=TransactionStatsResponse)
async def get_transaction_report(
    period: str = Path(..., regex="^(day|week|month|year)$"),
    date: Optional[datetime] = Query(None),
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    service = TransactionService(repo)
    stats = await service.get_stats_by_period(user_id, period, date)
    return stats

@router.get("/report/{period}", response_model=TransactionReportResponse)
async def get_transaction_report(
    period: str = Path(..., regex="^(day|week|month|year)$"),
    date: Optional[datetime] = Query(None),
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    service = TransactionService(repo)
    report = await service.get_descriptive_stats_by_period(user_id, period, date)
    return report

@router.get("/categories/{type}/{period}", response_model=TransactionStatsByCategoryResponse)
async def get_transactions_by_type_and_period(
    type: str = Path(..., regex="^(INCOME|EXPENSE)$"),
    period: str = Path(..., regex="^(day|week|month|year)$"),
    date: Optional[datetime] = Query(None),
    user_id: UUID4 = Depends(get_current_user_id),
    repo: TransactionRepository = Depends(get_transaction_repo)
):
    service = TransactionService(repo)
    return await service.get_transactions_by_type_and_period(user_id, type, period, date)