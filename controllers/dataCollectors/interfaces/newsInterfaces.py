from bson.json_util import dumps, ObjectId
import json, datetime

class newsInterfaces():
    def __init__(self, db):
        self.db = db
    def getAllRelevantKW(self):
        res = self.db.newsRelKW.find()
        raw = dumps(res)
        res = json.JSONDecoder().decode(raw)
        return res