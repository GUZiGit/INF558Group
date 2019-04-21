from pyld import jsonld
import json


f = open('usc.jsonld')
jsonObject = json.load(f)
f.close()

# print(jsonObject['@context'])
# print(jsonObject['@graph'])

jsonObject['@graph'].append({'@type':'ckb:UCLA','@id':'https://www.registrar.ucla.edu/Academics/Course-Descriptions','ckb:UniversityName':'UCLA'})




print(jsonObject['@context'])
print(jsonObject['@graph'])

outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('usc.jsonld','w')
f.write(outputFile)
f.close()
