from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.recurring_payment import RecurringPayment as RecurringPaymentModel
from app.schemas.recurring_payment_schema import RecurringPaymentCreate
from datetime import datetime


class RecurringPaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payment_data: RecurringPaymentCreate) -> RecurringPaymentModel:
        try:
            new_payment = RecurringPaymentModel(
                UserID=payment_data.user_id,
                CategoryID=payment_data.category_id,
                AccountID=payment_data.account_id,
                Name=payment_data.name,
                Amount=payment_data.amount,
                Frequency=payment_data.frequency.value,
                StartDate=payment_data.start_date,
                EndDate=payment_data.end_date
            )
            self.db.add(new_payment)
            await self.db.commit()
            await self.db.refresh(new_payment)
            return new_payment
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, payment_id: int) -> RecurringPaymentModel | None:
        try:
            result = await self.db.execute(
                select(RecurringPaymentModel).where(RecurringPaymentModel.PaymentID == payment_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e