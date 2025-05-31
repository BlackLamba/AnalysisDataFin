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
router.include_router(users_endpoint.router, tags=["users"])
router.include_router(auth_endpoint.router, tags=["auth"])
router.include_router(categories_endpoint.router, tags=["categories"])
router.include_router(transactions_endpoint.router, tags=["transactions"])
router.include_router(accounts_endpoint.router, tags=["accounts"])
router.include_router(budgets_endpoint.router, tags=["budgets"])
router.include_router(goals_endpoint.router, tags=["goals"])
router.include_router(recurrent_payments_endpoint.router, tags=["recurrent_payments"])