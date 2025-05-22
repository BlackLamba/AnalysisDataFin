from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.recurring_payment_schema import RecurringPaymentCreate, RecurringPayment
from app.services.recurring_payment_service import RecurringPaymentService
from app.db.session import get_db
from .base_endpoint import BaseRouter

router = BaseRouter(prefix="/recurrent-payments", tags=["recurrent_payments"]).router

@router.post("/", response_model=RecurringPayment, status_code=status.HTTP_201_CREATED)
async def create_recurrent_payment(
    payment_data: RecurringPaymentCreate,
    db: AsyncSession = Depends(get_db)
):
    service = RecurringPaymentService(db)
    return await service.create(payment_data=payment_data)

@router.get("/{payment_id}", response_model=RecurringPayment)
async def read_recurrent_payment(
    payment_id: str,
    db: AsyncSession = Depends(get_db)
):
    service = RecurringPaymentService(db)
    payment = await service.get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment