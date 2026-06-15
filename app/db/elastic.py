from elasticsearch import AsyncElasticsearch
from app.config import settings

# ElasticSearch client
es = None

async def connect():
    # initialize es 
    global es
    es = AsyncElasticsearch(settings.elastic_src)


async def disconnect():
    # close es 
    global es
    await es.close()