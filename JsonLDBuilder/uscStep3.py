import os
import sys
import json
from pyld import jsonld

from lxml.html.soupparser import fromstring

folderDir = 'USC'
fileList = os.listdir(folderDir)

f = open('usc.jsonld')
jsonObject = json.load(f)
f.close()

nextId = jsonObject['nextId']


nameToId = {}
nameToLink = {}
instructorObjs = []

for obj in jsonObject['@graph']:
    if obj['@type']=='ckb:Section' and 'ckb:InstructorID' in obj.keys() and 'ckb:InstructorLink' not in obj.keys():
        if obj['ckb:InstructorID'] in nameToId.keys():
            obj['ckb:InstructorID'] = nameToId[obj['ckb:InstructorID']]
        else:
            nameToId[obj['ckb:InstructorID']] = '_:'+ str(nextId)
            obj['ckb:InstructorID'] = '_:'+ str(nextId)
            nextId += 1
    if obj['@type']=='ckb:Section' and 'ckb:InstructorID' in obj.keys() and 'ckb:InstructorLink' in obj.keys():
        if obj['ckb:InstructorID'] in nameToId.keys():
            obj['ckb:InstructorID'] = nameToId[obj['ckb:InstructorID']]
            del obj['ckb:InstructorLink']
        else:
            nameToLink[obj['ckb:InstructorID']] = obj['ckb:InstructorLink']
            nameToId[obj['ckb:InstructorID']] = '_:'+ str(nextId)
            obj['ckb:InstructorID'] = '_:'+ str(nextId)
            nextId += 1
            del obj['ckb:InstructorLink']


for name in nameToId.keys():
    if name in nameToLink.keys():
        instructorObjs.append({'@id':nameToId[name],'@type':'ckb:Instructor','ckb:InstructorLink':nameToLink[name],'ckb:InstructorName':name})
    else:
        instructorObjs.append({'@id':nameToId[name],'@type':'ckb:Instructor','ckb:InstructorName':name})
            
    
jsonObject['@graph'] = jsonObject['@graph'] + instructorObjs

outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputObject['nextId'] = nextId
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('usc.jsonld','w')
f.write(outputFile)
f.close()
