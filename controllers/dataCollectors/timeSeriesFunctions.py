from flask_restful import Resource
from alpha_vantage.timeseries import TimeSeries
from controllers.controllerConstants import AV_API_KEY
from controllers.dataCollectors.interfaces.historicalDataInterfaces import HistoricalDataInterfaces

class TimeSeriesHistorical(Resource):
    def __init__(self, *urls, **kwargs):
        self.db = kwargs['db']
    def get(self, symbol, func):
        dbi = HistoricalDataInterfaces(self.db, symbol, func)
        meta = dbi.getMeta()
        if(len(meta) == 0):
            # No data in app. Get it from AVA
            ts = TimeSeries(key=AV_API_KEY)
            func = getattr(ts, func)
            data, meta_data = func(symbol)
            data, meta_data = dbi.addTimeSeries(data, meta_data)
        else:
            data, meta_data = dbi.getTimeSeries(meta)
        return {"meta": meta_data, "data": data }, 200

class TimeSeriesIntraday(Resource):
    def __init__(self, *urls, **kwargs):
        self.db = kwargs['db']
    def get(self, symbol, func):
        dbi = IntradayDataInterfaces(self.db, symbol, func)
        meta = dbi.getMeta()
        if(len(meta) == 0):
            # No data in app. Get it from AVA
            ts = TimeSeries(key=AV_API_KEY)
            func = getattr(ts, func)
            data, meta_data = func(symbol)
            data, meta_data = dbi.addTimeSeries(data, meta_data)
        else:
            data, meta_data = dbi.getTimeSeries(meta)
        return {"meta": meta_data, "data": data }, 200