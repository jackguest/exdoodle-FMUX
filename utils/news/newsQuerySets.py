from pymongo import MongoClient
from bson.json_util import dumps, ObjectId
import json, datetime
import numpy as np

year = '2018'
month = '3'

mongo_client=MongoClient('mongodb://localhost:27017')
db=mongo_client.tviztest

containerName = 'newYorkTimes{0}{1}'.format(year, month)
containerNameRelKW = containerName + 'RelKW'

oneDay = db[containerName].find()

raw = dumps(oneDay)
res = json.JSONDecoder().decode(raw)

count = 0
findWords = ['economy', 'finance', 'stock', 'market', 'crisis', 'terror', 'job', 'shareholder', 'elect']
db[containerNameRelKW].drop()
for i in res:
    kw = i['keywords'].lower()
    for j in findWords:
        if j in kw:
            rec = {}
            rec['date'] = i['date']
            rec['nid'] = i['_id']['$oid']
            rec['head'] = i['head']
            rec['main'] = i['main']
            if(rec['head'] == rec['main']):
                rec['head'] = ''
            rec['snippet'] = i['snippet']
            print(i['date'], '\n', i['head'], '\n', i['main'], '\n', i['snippet'], '\n', '************')
            db[containerNameRelKW].insert(rec)
            db.newsRelKW.insert(rec)
            count += 1
            break
print(count)