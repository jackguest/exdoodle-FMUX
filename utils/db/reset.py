from pymongo import MongoClient

mongo_client = MongoClient('mongodb://0.0.0.0:27017')
db = mongo_client.tviztest

db.stockTimeSeriesMeta.remove({})
db.stockTimeSeries.remove({})