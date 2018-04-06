from flask_restful import Resource
from alpha_vantage.timeseries import TimeSeries
from controllers.controllerConstants import AV_API_KEY

class AdhocStockTest(Resource):
    def get(self, symbol, func):
        ts = TimeSeries(key=AV_API_KEY)
        func = getattr(ts, func)
        data = func(symbol, interval="1min")
        return { "data": data[0], "meta": data[1] } , 200

