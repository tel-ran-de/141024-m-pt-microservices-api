from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings


# создание движка с пулом подключений
engine = create_async_engine(
    settings.async_database_url,
    pool_size=5,          # Сколько соединений держать всегда открытыми
    max_overflow=10,      # Сколько доп. соединений открыть при пиковой нагрузке
    pool_timeout=30,      # Как долго ждать освобождения коннекта (сек)
    pool_recycle=1800,    # Время жизни одного соединения (секунды)
    echo=False,            # (опционально) логирует SQL-запросы
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
