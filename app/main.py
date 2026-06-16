from fastapi import FastAPI
from app.db import mongo, elastic

app = FastAPI()

@app.on_event("startup")
async def startup():
    # connect to both databases 
    await mongo.connect()
    await elastic.connect()

@app.on_event("shutdown")
async def shutdown():
    # disconnect from both databases 
    await mongo.disconnect()
    await elastic.disconnect()