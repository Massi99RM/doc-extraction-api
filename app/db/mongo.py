from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db = None

async def connect():
    # initialize client and db here
    global client, db
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client["invoices"]

async def disconnect():
    # close the client here
    global client
    client.close()