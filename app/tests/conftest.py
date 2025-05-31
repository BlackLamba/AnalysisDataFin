import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.main import app as application
from app.core.config import Settings
import os
import copy


class TestSettings(Settings):
    def __init__(self):
        super().__init__()
        self.POSTGRES_SERVER = "localhost"
        self.POSTGRES_USER = "postgres"
        self.POSTGRES_PASSWORD = "admin"
        self.POSTGRES_DB = "Finomic_test"
        self.SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" \
                                       f"{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}"


# Заменяем оригинальные настройки на тестовые
from app.core import config
config.settings = TestSettings()


@pytest.fixture
def app():
    yield application


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac