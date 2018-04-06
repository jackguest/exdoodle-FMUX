import json
from random import randint
from utilsConstants import NYT_API_KEY
import requests

def getMonthNYTimes(year, month):
    url = 'http://api.nytimes.com/svc/archive/v1'

    response = requests.get('{0}/{1}/{2}.json?api-key={3}'.format(url, year, month, NYT_API_KEY))
    tjson = response.content

    tjson = tjson.decode('utf-8')

    tjson = json.loads(tjson)
    docs = tjson['response']['docs']

    recs = 0
    ph = 0
    limit = 0
    data = []
    keywordsList = []
    kickersList = []
    typesList = []

    for i in docs:
        entry = {}
        recs += 1
        if 'headline' in i:
            entry['head'] = ''
            if 'print_headline' in i['headline'] and i['headline']['print_headline'] != None:
                entry['head'] = i['headline']['print_headline']
            entry['main'] = ''
            if 'main' in i['headline'] and i['headline']['main'] != None:
                entry['main'] = i['headline']['main']
            entry['kicker'] = ''
            if 'kicker' in i['headline'] and i['headline']['kicker'] != None:
                entry['kicker'] = i['headline']['kicker']
                if i['headline']['kicker'] not in kickersList:
                    kickersList.append(i['headline']['kicker'])

            ph += 1
        entry['snippet'] = ''
        if 'snippet' in i and i['snippet'] != None:
            entry['snippet'] = i['snippet']
        entry['date'] = ''
        if 'pub_date' in i and i['pub_date'] != None:
            entry['date'] = i['pub_date'].split('T')[0]
        entry['type'] = ''
        if 'type_of_material' in i and i['type_of_material'] != None:
            entry['type'] = i['type_of_material']
            if(i['type_of_material']) not in typesList:
                typesList.append(i['type_of_material'])
        entry['keywords'] = ''
        if 'keywords' in i and len(i['keywords']) > 0:
            strVal = ''
            l = len(i['keywords']) - 1
            for x in range(len(i['keywords'])):
                if 'value' in i['keywords'][x]:
                    a = i['keywords'][x]['value']
                    if a not in keywordsList:
                        keywordsList.append(a)
                    if x != l:
                        a += ' | '
                    strVal += a
            entry['keywords'] = strVal

        data.append(entry)

    print('RECS', recs)
    print('PH', ph)
    print('KW', len(keywordsList))
    print('KICKERS', len(kickersList))
    print('TYPES', len(typesList))

    r = randint(0, recs-1)
    for i in range(len(data)-1):
        if limit == r:
            for key in data[i]:
                print(key, ":", data[i][str(key)])
            print('************************   ', r)

        limit += 1

    return data

year = '2018'
month = '3'

data = getMonthNYTimes(year, month)
print('DOCS COUNT', len(data))

containerName = 'newYorkTimes{0}{1}'.format(year, month)

from pymongo import MongoClient
mongo_client=MongoClient('mongodb://localhost:27017')
db=mongo_client.tviztest

db[containerName].drop()
for i in data:
    db[containerName].insert(i)

