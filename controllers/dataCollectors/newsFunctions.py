from flask_restful import Resource
from controllers.dataCollectors.interfaces.newsInterfaces import newsInterfaces

class newsAllRelKW(Resource):
    def __init__(self, *urls, **kwargs):
        self.db = kwargs['db']
    def get(self):
        dbi =  newsInterfaces(self.db)
        data = dbi.getAllRelevantKW()
        if(len(data) == 0):
            # No data in app. Run news utilities
            data = "No Data"
            status = 404
        else:
            status = 200
        return {"data": data }, status
