from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.bank_account import BankAccount as BankAccountModel
from app.schemas.bank_account_schema import BankAccountCreate
import uuid


class BankAccountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, account_data: BankAccountCreate) -> BankAccountModel:
        try:
            new_account = BankAccountModel(
                AccountID=uuid.uuid4(),
                UserID=account_data.user_id,
                AccountNumber=account_data.account_number,
                BankName=account_data.bank_name,
                Currency=account_data.currency,
                IsActive=account_data.is_active,
                Balance=0.0  # можно явно указать, если не передаётся в Create
            )
            self.db.add(new_account)
            await self.db.commit()
            await self.db.refresh(new_account)
            return new_account
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Account with this number already exists for the user.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get(self, account_id: str) -> BankAccountModel | None:
        try:
            result = await self.db.execute(
                select(BankAccountModel).where(BankAccountModel.AccountID == account_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e