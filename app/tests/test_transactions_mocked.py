from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import UUID

client = TestClient(app)


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.transactions_endpoint.get_transaction_repo")
async def test_get_transaction_by_id(mock_get_repo):
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = {
        "TransactionID": UUID("123e4567-e89b-12d3-a456-426614174000"),
        "UserID": UUID("a12f3456-7890-12d3-a456-426614174000"),
        "Amount": -100.0
    }

    with patch("app.api.v1.endpoints.transactions_endpoint.get_transaction_repo", return_value=mock_repo):
        response = client.get("/transactions/123e4567-e89b-12d3-a456-426614174000")

    assert response.status_code == 200
    assert response.json()["Amount"] == -100.0