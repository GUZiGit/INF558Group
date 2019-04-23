import os
import re
import json
from pyld import jsonld
from lxml import html, etree
# from lxml.html.soupparser import fromstring
folderDir = 'UCLA/'
fileList = os.listdir(folderDir)
f = open('ucla.jsonld')
jsonObject = json.load(f)
f.close()
nextId = jsonObject['nextId']
courses = []
for d in fileList:    
    if d=='main.html':
        continue
    fileDir = 'UCLA/'+d
    f = open(fileDir,'r')
    
    url = f.readline()
    content = f.read()
    tree = html.fromstring(content)

    programName = tree.xpath('//div[@class="page-header"]//span/text()')
    if len(programName)<1:
        continue
    programName = programName[0]
    if "(" in programName:
        programName=re.sub("[\(\[].*?[\)\]]", "", str(programName))
        programName=programName[0:len(programName)-2]
    programJsonObj = {'@id':url[:-1],'@type':'ckb:Program','UniversityName':'UCLA','ckb:hasCourses':[],'ckb:ProgramName':programName,'ckb:UniversityName':'UCLA'}
    for i in tree.xpath('//div[@class="tab-pane"]/ul/li/div'):
            courseName=i.xpath('h3/text()')[0]
            unit=i.xpath('p[1]/text()')[0]
            description=i.xpath('p[2]/text()')
            if not description:
                description=""
            else:
                description=description[0]
            aCourseJsonObj = {'ckb:ProgramName':programName,'@id':'_:'+str(nextId),'@type':'ckb:Course','ckb:UniversityName':'UCLA','ckb:CourseName':courseName,'ckb:Unit':unit,'ckb:Description':description}
            programJsonObj['ckb:hasCourses'].append('_:'+str(nextId))
            nextId += 1
            courses.append(aCourseJsonObj)
    courses.append(programJsonObj)
    
    # for aCourse in tree.xpath('//div[@class="course-table"]/div'):

    #     courseAbbre=aCourse.xpath('div/h3/a/strong/text()')[0][:-1]

    #     courseName=aCourse.xpath('div/h3/a/text()')[0]
        
    #     description=aCourse.xpath('div[2]/div[@class="catalogue"]/text()')

    #     description = description[0] if len(description)>0 else ''

    #     aCourseJsonObj = {'ckb:ProgramName':programName,'@id':'_:'+str(nextId),'@type':'ckb:Course','ckb:UniversityName':'UCLA','ckb:CourseName':courseName,'ckb:Description':description}
    #     programJsonObj['ckb:hasCourses'].append('_:'+str(nextId))
        
    #     nextId += 1
        
#         print(aCourseJsonObj)
    #     courses.append(aCourseJsonObj)
    # courses.append(programJsonObj)

jsonObject['@graph'] = jsonObject['@graph']+courses

outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputObject['nextId'] = nextId
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('ucla.jsonld','w')
f.write(outputFile)
f.close()