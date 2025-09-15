from sqlalchemy import text, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import src.config as config

engine = create_async_engine(
    config.DATABASE_URL,
    poolclass=NullPool,
)

# фабрика сессий
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# базовый класс для моделей
class Base(DeclarativeBase):
    pass

# dependency для FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session


