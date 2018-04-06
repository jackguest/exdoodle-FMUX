import csv
import json
import sys, getopt, pprint
import os
from pymongo import MongoClient
mongo_client=MongoClient('mongodb://localhost:27017')
db=mongo_client.tviztest
healthServicesCompanies = db.nasdaqCompanies.find(
    {"industry": "Major Pharmaceuticals"}
).sort("Name")

count = 0
for co in healthServicesCompanies:
    print(co["Symbol"], co["Name"])
    count += 1

print(count)
