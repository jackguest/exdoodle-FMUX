import csv
import json
import sys, getopt, pprint
import os
from pymongo import MongoClient
#CSV to JSON Conversion
workDir = os.path.dirname(os.path.realpath(__file__))

csvfile = open('{0}/nasdaqCompanyList.csv'.format(workDir), 'r')
reader = csv.DictReader( csvfile )
mongo_client=MongoClient('mongodb://localhost:27017')
db=mongo_client.tviztest


db.nasdaqCompanies.drop()

for key in reader:
    bad = False
    for val in key:
        if val == None:
            bad = True
            continue

    if(bad == True):
        key.pop(None)

    db.nasdaqCompanies.insert(key)


