import pytest
from httpx import AsyncClient
from app.main import app
from uuid import UUID
from fastapi import status


@pytest.mark.asyncio
async def test_get_transaction_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        transaction_id = "bbba1a10-4d3e-4b8a-9841-2bb047d3de48"
        response = await ac.get(f"/transactions/{transaction_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_period_stats():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldmdlbnlieWNoa292M0BnbWFpbC5jb20iLCJ1c2VyX2lkIjoiN2YwZWMwNzEtODc2NS00ZmFhLWFiMzUtZjRhODYxMDI5OTk5IiwiZXhwIjoxNzQ4NDE1NDEzfQ.cSXvnv9ovVh4lwX8jyMz3Vhd5AL2h7UquPI7aPkFCxg"}
        response = await ac.get("/transactions/stats/period/day", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_expenses_by_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldmdlbnlieWNoa292M0BnbWFpbC5jb20iLCJ1c2VyX2lkIjoiN2YwZWMwNzEtODc2NS00ZmFhLWFiMzUtZjRhODYxMDI5OTk5IiwiZXhwIjoxNzQ4NDE1NDEzfQ.cSXvnv9ovVh4lwX8jyMz3Vhd5AL2h7UquPI7aPkFCxg"}
        response = await ac.get("/transactions/expenses/categories?period=month", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_income_by_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldmdlbnlieWNoa292M0BnbWFpbC5jb20iLCJ1c2VyX2lkIjoiN2YwZWMwNzEtODc2NS00ZmFhLWFiMzUtZjRhODYxMDI5OTk5IiwiZXhwIjoxNzQ4NDE1NDEzfQ.cSXvnv9ovVh4lwX8jyMz3Vhd5AL2h7UquPI7aPkFCxg"}
        response = await ac.get("/transactions/income/categories?period=year", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND