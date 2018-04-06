from flask_restful import Resource
from bson.json_util import dumps
import json

class GetNasdagCompanyList(Resource):
    def __init__(self, *urls, **kwargs):
        self.db = kwargs['db']
    def get(self):
        healthServicesCompanies = self.db.nasdaqCompanies.find()
        raw = dumps(healthServicesCompanies)
        res = json.JSONDecoder().decode(raw)
        return res, 200
