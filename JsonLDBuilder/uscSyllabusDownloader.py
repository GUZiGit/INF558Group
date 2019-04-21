import os
import sys
import json
from pyld import jsonld
from lxml.html.soupparser import fromstring
import re
import urllib
# response = urllib2.urlopen('http://www.example.com/')
# html = response.read()

folderDir = 'USC'
fileList = os.listdir(folderDir)

f = open('usc.jsonld')
jsonObject = json.load(f)
f.close()

nextId = jsonObject['nextId']


syllabusList = os.listdir('USC/syllabus')

for obj in jsonObject['@graph']:
    if 'ckb:Syllabus' in obj.keys() and obj['ckb:Syllabus']=='PDF':
        
        if obj['ckb:sectionID']+'.pdf' in syllabusList:
            continue
        
#         print(obj['ckb:SyllabusLink'])
        response = urllib.request.urlopen(obj['ckb:SyllabusLink'])
        data = response.read()
#         content = data.encode('ISO-8859-1')
#         print(content)
#         print(data.decode('ISO-8859-1'))
        f = open('USC/syllabus/'+obj['ckb:sectionID']+'.pdf', 'wb')
        f.write(data)
        f.close()
    if 'ckb:Syllabus' in obj.keys() and obj['ckb:Syllabus']=='Word':
        
        if obj['ckb:sectionID']+'.doc' in syllabusList:
            continue
#         print(obj['ckb:SyllabusLink'])
        response = urllib.request.urlopen(obj['ckb:SyllabusLink'])
        data = response.read()
#         content = data.encode('ISO-8859-1')
#         print(content)
#         print(data.decode('ISO-8859-1'))
        f = open('USC/syllabus/'+obj['ckb:sectionID']+'.doc', 'wb')
        f.write(data)
        f.close()


