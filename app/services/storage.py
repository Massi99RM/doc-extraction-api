from app.db import mongo
from bson import ObjectId
from fastapi import HTTPException
from bson.errors import InvalidId

COLLECTION_NAME = "invoice_collection"

async def save_invoice(invoice_data: dict):
    try:
        database = mongo.db[COLLECTION_NAME]
        collection = await database.insert_one(invoice_data)
        return collection.inserted_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_invoice(invoice_id: str):
    try:
        database = mongo.db[COLLECTION_NAME]
        found = await database.find_one({"_id": ObjectId(invoice_id)})
        return found
    except InvalidId as e:
        raise HTTPException(status_code=400, detail=f"Invalid invoice ID: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")