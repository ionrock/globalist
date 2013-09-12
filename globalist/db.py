from config import config
import pymongo


def get_conn():
    return pymongo.MongoClient(
        config.get('mongo_uri', 'mongodb://localhost:27017/')
    )
