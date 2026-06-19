from app.db import mongo
from bson import ObjectId

COLLECTION_NAME = "invoice_collection"

async def save_invoice(invoice_data: dict):
    # insert invoice_data into the mongo collection, return the inserted id
    database = mongo.db[COLLECTION_NAME]
    collection = await database.insert_one(invoice_data)
    return collection.inserted_id

async def get_invoice(invoice_id: str):
    # fetch one invoice by id from the mongo collection
    database = mongo.db[COLLECTION_NAME]
    found = await database.find_one({"_id": ObjectId(invoice_id)})
    return found