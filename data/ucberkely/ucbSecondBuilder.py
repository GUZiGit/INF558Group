import os
import re
import json
from pyld import jsonld
from lxml import html, etree
# from lxml.html.soupparser import fromstring
folderDir = 'UCBerkely/'
fileList = os.listdir(folderDir)
f = open('ucb.jsonld')
jsonObject = json.load(f)
f.close()
nextId = jsonObject['nextId']
courses = []
for d in fileList:    
    if d=='main.html':
        continue
    fileDir = 'UCBerkely/'+d
    f = open(fileDir,'r')
    
    url = f.readline()
    content = f.read()
    tree = html.fromstring(content)

    programName = tree.xpath('//h1[@class="page-header"]/text()')
    if len(programName)<1:
        continue
    programName = programName[0]
    if "(" in programName:
        programName=re.sub("[\(\[].*?[\)\]]", "", str(programName))
        programName=programName[0:len(programName)-2]
    programJsonObj = {'@id':url[:-1],'@type':'ckb:Program','UniversityName':'UCBerkely','ckb:hasCourses':[],'ckb:ProgramName':programName,'ckb:UniversityName':'UCBerkely'}
    for i in tree.xpath('//div[@class="courseblock"]'):
            code=i.xpath('button/h3/span[@class="code"]/text()')[0]
            code = str(code).replace("\u00a0", " ")
            courseName=i.xpath('button/h3/span[@class="title"]/text()')[0]
            unit=i.xpath('button/h3/span[@class="hours"]/text()')[0]
            description=i.xpath('div[@class="coursebody"]/p/span/text()')
            # print(description) 
            # if not description:
            #     description=""
            if len(description)<2:
                description=""
            else:
                description=description[1][1:]
            aCourseJsonObj = {'ckb:ProgramName':programName,'@id':'_:'+str(nextId),'@type':'ckb:Course','ckb:UniversityName':'UCBerkely','ckb:CourseName':courseName,'ckb:Unit':unit,'ckb:Description':description,'ckb:code':code}
            programJsonObj['ckb:hasCourses'].append('_:'+str(nextId))
            nextId += 1
            courses.append(aCourseJsonObj)
    courses.append(programJsonObj)

jsonObject['@graph'] = jsonObject['@graph']+courses

outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputObject['nextId'] = nextId
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('ucb.jsonld','w')
f.write(outputFile)
f.close()