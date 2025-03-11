import pytest
import pytest_asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from database import get_db
from main import app
from httpx import ASGITransport, AsyncClient

# TEST_DATABASE_URL = "postgresql+asyncpg://test-user:password@localhost:5434/test_db"


@pytest.fixture(scope="session")
def test_db_url():
    """Собирает URL тестовой базы данных из .env.local."""
    load_dotenv(".env.local")
    db_user = os.getenv("TEST_DB_USER")
    db_password = os.getenv("TEST_DB_PASSWORD")
    db_host = os.getenv("TEST_DB_HOST")
    db_port = os.getenv("TEST_DB_PORT")
    db_name = os.getenv("TEST_DB_NAME")

    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError(
            "Не все необходимые переменные окружения для тестовой БД заданы в .env.local"
        )

    db_url = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return db_url


@pytest_asyncio.fixture
async def test_db(test_db_url):
    engine = create_async_engine(test_db_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncTestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(test_db):
    # Переопределяем зависимость get_db
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    # Используем AsyncClient
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
