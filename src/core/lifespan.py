from starlette.applications import Starlette
from contextlib import asynccontextmanager
from orm import Base, engine

@asynccontextmanager
async def lifespan(app: Starlette):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
