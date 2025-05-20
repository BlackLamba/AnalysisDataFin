from fastapi import APIRouter
from app.api.v1.endpoints import (
    users_endpoint,
    auth_endpoint,
    categories_endpoint,
    transactions_endpoint,
    accounts_endpoint,
    budgets_endpoint,
    goals_endpoint,
    recurrent_payments_endpoint
)

router = APIRouter()

# Подключаем все endpoint-ы версии v1
router.include_router(users_endpoint.router, prefix="/users", tags=["users"])
router.include_router(auth_endpoint.router, prefix="/auth", tags=["auth"])
router.include_router(categories_endpoint.router, prefix="/categories", tags=["categories"])
router.include_router(transactions_endpoint.router, prefix="/transactions", tags=["transactions"])
router.include_router(accounts_endpoint.router, prefix="/accounts", tags=["accounts"])
router.include_router(budgets_endpoint.router, prefix="/budgets", tags=["budgets"])
router.include_router(goals_endpoint.router, prefix="/goals", tags=["goals"])
router.include_router(recurrent_payments_endpoint.router, prefix="/recurrent_payments", tags=["recurrent_payments"])