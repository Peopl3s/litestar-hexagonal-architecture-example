import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from postgres.models.base import Base

# Настройка тестовой БД
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/exhibit_test_db"

# Создаем новый событийный цикл, который будет использоваться для запуска асинхронных тестов.
@pytest_asyncio.fixture(scope="session") # Параметр scope="session" означает, что событийный цикл будет создан один раз на всю сессию тестирования, а не для каждого теста отдельно
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

# Фикстура для движка базы данных
@pytest_asyncio.fixture(scope="session")
async def db_engine():
    # Создает движок с подключением к тестовой базе данных
    engine = create_async_engine(TEST_DATABASE_URL, echo=True) # Параметр echo=True включает вывод SQL-запросов в консоль для отладки.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) #Создает все таблицы в базе данных с помощью Base.metadata.create_all.
    yield engine # Выдает движок для использования в тестах.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # После завершения тестов удаляет все таблицы (Base.metadata.drop_all)
    await engine.dispose() # и освобождает ресурсы движка (engine.dispose()).

# Фикстура для сессии базы данных
@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncSession:
    async with AsyncSession(db_engine) as session: # Создает новую сессию базы данных.
        yield session # Выдает сессию для использования в тестах.
        await session.rollback() # После завершения теста откатывает все изменения (session.rollback()), чтобы база данных оставалась в исходном состоянии.
