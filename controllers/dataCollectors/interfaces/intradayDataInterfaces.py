from alpha_vantage.timeseries import TimeSeries
from controllers.controllerConstants import AV_API_KEY
from bson.json_util import dumps, ObjectId
import json, datetime
import numpy as np

class IntradayDataInterfaces():
    def __init__(self, db, symbol, func):
        self.db = db
        self.func = func
        self.symbol = symbol = symbol.upper()
        self.localMeta = {}
    def getMeta(self):
        self.stsmResults = self.db.stockTimeSeriesMeta.find({
            'symbol': self.symbol,
            'function': self.func
        })
        raw = dumps(self.stsmResults)
        res = json.JSONDecoder().decode(raw)
        return res
    def addTimeSeries(self, data, meta_data):
        # Format AVA data to App Data
        self.localMeta['refresh'] = meta_data['3. Last Refreshed']
        fd = self.dataParser('TIME_SERIES', data, meta_data)
        fmd = self.dataParser('TIME_SERIES_META', data, meta_data)
        # Go ahead and insert Meta Document
        self.stsMetaResults = self.db.stockTimeSeriesMeta.insert(fmd)
        # Convert Meta Docs ObjectId for JSON return and Adding as ['metaId'] in Data
        idRaw = dumps(fmd['_id'])
        oid = json.JSONDecoder().decode(idRaw)
        fmd['_id'] = oid['$oid']
        for i in range(len(fd)):
            fd[i]['metaId'] = fmd['_id']
        # Add the data and convert Object for JSON return and add metaId
        self.stsDataResults = self.db.stockTimeSeries.insert(fd)
        for id in fd:
            idRaw = dumps(id['_id'])
            oid = json.JSONDecoder().decode(idRaw)
            id['_id'] = oid['$oid']
        # Return Data and MetaData for API response
        return fd, fmd
    def getTimeSeries(self, meta):
        # Convert Meta Docs ObjectId for JSON return and Adding as ['metaId'] in Data
        idRaw = dumps(meta[0]['_id'])
        oid = json.JSONDecoder().decode(idRaw)
        meta[0]['_id'] = oid['$oid']
        self.localMeta['refresh'] = meta[0]['refresh']
        stsResults = self.db.stockTimeSeries.find({ 'metaId': meta[0]['_id']})
        raw = dumps(stsResults)
        res = json.JSONDecoder().decode(raw)
        for id in res:
            idRaw = dumps(id['_id'])
            oid = json.JSONDecoder().decode(idRaw)
            id['_id'] = oid['$oid']
        return res, meta[0]
    def dataParser(self, type, data, meta_data):
        if(type == 'TIME_SERIES_META'):
            formattedMetaData = {
                'symbol': self.symbol,
                'function': self.func,
                'timeZone': meta_data['4. Time Zone'],
                'refresh': meta_data['3. Last Refreshed']
            }
            formattedMetaData = self.applyFuncMetaDataRules(formattedMetaData)

            return formattedMetaData
        elif(type == 'TIME_SERIES'):
            formattedData = []
            for key in data:
                vol = float(data[key]['6. volume'])
                adjClose = float(data[key]['5. adjusted close'])
                div = float(data[key]['7. dividend amount'])
                low = float(data[key]['3. low'])
                high = float(data[key]['2. high'])
                # Calculate Local Meta Data from bulk data
                self.localMeta['volumes'] = np.append(self.localMeta['volumes'], vol)
                self.localMeta['adjCloses'] = np.append(self.localMeta['adjCloses'], adjClose)
                self.localMeta['dateRange'].append(key);
                self.localMeta['mLows'] = np.append(self.localMeta['mLows'], low)
                self.localMeta['mHighs'] = np.append(self.localMeta['mHighs'], high)
                if(div) > 0:
                    self.localMeta['divsPaid'] = np.append(self.localMeta['divsPaid'], div)
                if(key == self.localMeta['refresh']):
                    self.localMeta['lastAdjustedClose'] = adjClose
                elem = {
                    'metaId': '',
                    'date': key,
                    'close': float(data[key]['4. close']),
                    'volume': vol,
                    'open': float(data[key]['1. open']),
                    'dividend': div,
                    'adjustedClose': adjClose,
                    'low': low,
                    'high': high
                }
                formattedData.append(elem)
            return formattedData

        return 0
    def applyFuncMetaDataRules(self, formattedMetaData):

        return formattedMetaData