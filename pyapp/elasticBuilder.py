import os
import sys
import json
from pyld import jsonld
import requests
import json
import elasticsearch
import elasticsearch_dsl

from lxml.html.soupparser import fromstring

# folderDir = 'USC'
# fileList = os.listdir(folderDir)

f = open('usc.jsonld')
jsonObject = json.load(f)
f.close()

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])


for obj in jsonObject:
    es.index(index='usc',body=obj,doc_type='json')





