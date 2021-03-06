from pyld import jsonld
import json

context = {}
document = []

context['ckb'] = 'http://www.semanticweb.org/rice/ontologies/2019/3/CourseKB'
context['xsd'] = 'http://www.w3.org/2001/XMLSchema'
# context['nextid'] = '1'


document.append({'@id':'_:0','@type':'ckb:University'})
document.append({'@id':'https://www.registrar.ucla.edu/Academics/Course-Descriptions','@type':'ckb:UCLA','ckb:UniversityName':'UCLA'})
# document.append({'@id':'a blank node id','oc:something':'some where'})

outputJson = jsonld.compact(document,context)
outputJson['nextId'] = 1

outputString = json.dumps(outputJson,indent = 2)
file = open('ucla.jsonld','w')
file.write(outputString)
file.close()

