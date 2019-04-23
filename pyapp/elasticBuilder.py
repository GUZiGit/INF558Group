import os
import sys
import json
from pyld import jsonld
import requests
import json
import elasticsearch
import elasticsearch_dsl

# from lxml.html.soupparser import fromstring

# folderDir = 'USC'
# fileList = os.listdir(folderDir)

f = open('ucb.jsonld')
jsonObject = json.load(f)
f.close()

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])


for i in range(len(jsonObject)):
    es.index(index='uscfinal',body=jsonObject[i],doc_type='json')
    if i%1000==0:
        print(i)

