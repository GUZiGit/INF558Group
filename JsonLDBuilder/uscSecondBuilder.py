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


courses = []
for d in fileList:
    
    if d=='main.html':
        continue
    

    
    fileDir = 'USC/'+d
    f = open(fileDir,'r')
    
    url = f.readline()
    content = f.read()
    tree = fromstring(content)
    
    programName = tree.xpath('//h2[@class="dept-title"]/text()')
    if len(programName)<1:
        continue
    programName = programName[0]
    
    programJsonObj = {'@id':url[:-1],'@type':'ckb:Program','UniversityName':'USC','ckb:hasCourses':[],'ckb:ProgramName':programName,'ckb:UniversityName':'USC'}
    
    for aCourse in tree.xpath('//div[@class="course-table"]/div'):

        courseAbbre=aCourse.xpath('div/h3/a/strong/text()')[0][:-1]

        courseName=aCourse.xpath('div/h3/a/text()')[0]
        
        description=aCourse.xpath('div[2]/div[@class="catalogue"]/text()')

        description = description[0] if len(description)>0 else ''

        aCourseJsonObj = {'ckb:ProgramName':programName,'@id':'_:'+str(nextId),'@type':'ckb:Course','ckb:UniversityName':'USC','ckb:CourseAbbre':courseAbbre,'ckb:CourseName':courseName,'ckb:Description':description}
        programJsonObj['ckb:hasCourses'].append('_:'+str(nextId))
        
        nextId += 1
        
#         print(aCourseJsonObj)
        courses.append(aCourseJsonObj)
    courses.append(programJsonObj)

jsonObject['@graph'] = jsonObject['@graph']+courses

outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputObject['nextId'] = nextId
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('usc.jsonld','w')
f.write(outputFile)
f.close()