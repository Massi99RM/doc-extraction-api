from fastapi import FastAPI
from app.api.routes import ingest, search
from app.db import mongo, elastic
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: connect
    try:
        # connect to both databases
        await mongo.connect()
        await elastic.connect()
        yield
    # shutdown: disconnect
    finally:
        # disconnect from both databases
        await mongo.disconnect()
        await elastic.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(search.router)
app.include_router(ingest.router)


