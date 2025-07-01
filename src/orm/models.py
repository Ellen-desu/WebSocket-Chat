from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker

from datetime import datetime
from zoneinfo import ZoneInfo
from configs import database_echo, zone_info

_SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///data/database.db"

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(144), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(ZoneInfo(zone_info)).replace(microsecond=0))
    

engine: create_async_engine = create_async_engine(_SQLALCHEMY_DATABASE_URI, echo=database_echo)

async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)