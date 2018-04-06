from flask_restful import Api
from controllers.todos import Todo, TodoList
from controllers.dataCollectors.adhoc import AdhocStockTest
from controllers.dataCollectors.nasdaqCompanyList import GetNasdagCompanyList
from pymongo import MongoClient
from controllers.dataCollectors.timeSeriesFunctions import TimeSeriesHistorical, TimeSeriesIntraday
from controllers.dataCollectors.newsFunctions import newsAllRelKW

class GlobalDefs():
    def __init__(self, app, globals):
        self.api = Api(app)
        self.globals = globals
        self.mongo_client = MongoClient('mongodb://0.0.0.0:27017')
        self.db = self.mongo_client.tviztest
        self.AddResources(self.db)

    def AddResources(self, db):
        ## Actually setup the Api resource routing here
        self.api.add_resource(TimeSeriesHistorical,
                              '/tss/<symbol>/<func>',
                              resource_class_kwargs={
                                  'db':db
                              })
        self.api.add_resource(newsAllRelKW,
                              '/nrakw',
                              resource_class_kwargs={
                                  'db':db
                              })
        self.api.add_resource(TimeSeriesIntraday,
                              '/tsid/<symbol>/<func>',
                              resource_class_kwargs={
                                  'db':db
                              })


        # Utility Resources
        self.api.add_resource(GetNasdagCompanyList,
                              '/gncl',
                              resource_class_kwargs={
                                  'db':db
                              })

        #Test Functions
        self.api.add_resource(TodoList, '/todos',
                              resource_class_kwargs={
                                  'db':db
                              })
        self.api.add_resource(Todo, '/todos/<todo_id>')
        self.api.add_resource(AdhocStockTest,
                              '/ast/<symbol>/<func>')
