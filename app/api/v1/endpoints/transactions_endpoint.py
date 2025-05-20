from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction_schema import TransactionCreate, TransactionOut
from app.services.transaction_service import TransactionService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/transactions", tags=["transactions"]).router

@router.post("/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    service = TransactionService(db)
    return await service.create(transaction_data=transaction_data)

@router.get("/{transaction_id}", response_model=TransactionOut)
async def read_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = TransactionService(db)
    transaction = await service.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction