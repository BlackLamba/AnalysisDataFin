from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bank_account_schema import BankAccountCreate, BankAccount
from app.services.bank_account_service import BankAccountService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/accounts", tags=["accounts"]).router

@router.post("/", response_model=BankAccount, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: BankAccountCreate,
    db: AsyncSession = Depends(get_db)
):
    service = BankAccountService(db)
    return await service.create(account_data=account_data)

@router.get("/{account_id}", response_model=BankAccount)
async def read_account(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = BankAccountService(db)
    account = await service.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account