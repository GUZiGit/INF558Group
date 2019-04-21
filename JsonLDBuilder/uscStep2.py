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
        nextId += 1
        
        programJsonObj['ckb:hasCourses'].append('_:'+str(nextId))
        nextId += 1
        
        aCourseJsonObj['ckb:sections'] = []
        
#         table = aCourse.xpath('//table[@class="sections responsive"]')[0]
        table = aCourse.xpath('div[2]/table[@class="sections responsive"]')[0].getchildren()
        tableIndex = list(map(lambda c: c.text,table[0].getchildren()))
        
        for i in range(1,len(table)):
            
            aSection = {'@id':'_:'+str(nextId),'@type':'ckb:Section'}
            nextId += 1
            
            ths = table[i].getchildren()
#             print(ths[0].text)
            aSection['ckb:sectionID']= ths[0].text
            if len(ths)>1 and len(ths[1].getchildren())>0:
                aSection['ckb:sessionID']=ths[1].getchildren()[0].text
                aSection['ckb:sessionLink']=ths[1].getchildren()[0].xpath('@href')[0]
#                 print(ths[1].getchildren()[0].text)
#                 print(ths[1].getchildren()[0].xpath('@href')[0])
            if len(ths)>1 and len(ths[1].getchildren())<=0:
#                 print(ths[1].text)
                aSection['ckb:sessionID']=ths[1].text
#             if len(ths)<1:
#                 print('None')
#                 aSection['ckb:sessionID':'']

            if len(ths)>2:
                aSection['ckb:sessionType']=ths[2].text
#                 print(ths[2].text)
                
            
            if len(ths) > 3:
#                 print(ths[3].text)
                aSection['ckb:Time']=ths[3].text
                
            if len(ths)>4:
#                 print(ths[4].text)
                aSection['ckb:Days']=ths[4].text
                
            if len(ths)>6 and ths[6].text == None:
                if len(ths[6].getchildren()) > 0 and len(ths[6].getchildren()) <2 :
#                     print(ths[6].getchildren()[0].text)
                    aSection['ckb:InstructorID']=ths[6].getchildren()[0].text
#                     print(ths[6].getchildren()[0].xpath('@href')[0])
                    aSection['ckb:InstructorLink']=ths[6].getchildren()[0].xpath('@href')[0]
                else:
#                     print('None')
                    pass
            else:
                if len(ths)>5:
                    aSection['ckb:InstructorID']=ths[6].text
#                 print('None' if len(ths)<=5 else ths[6].text)
#             print()
            
            if len(ths)>7 and len(ths[7].getchildren())>1:
#                 print(ths[7].getchildren()[0].text)
                aSection['ckb:Location'] = ths[7].getchildren()[0].text
            if len(ths)>7 and len(ths[7].getchildren())<1:
#                 print(ths[7].text)
                aSection['ckb:Location'] = ths[7].text
#             if len(ths)<=7:
#                 print('None')
            if len(ths)>8 and len(ths[8].getchildren())>1:
#                 print(ths[8].getchildren()[0].text)
                aSection['ckb:Syllabus'] = ths[8].getchildren()[0].text
#                 print(ths[8].getchildren()[0].xpath('@href')[0])
                aSection['ckb:SyllabusLink'] = ths[8].getchildren()[0].xpath('@href')[0]
            
            aCourseJsonObj['ckb:sections'].append(aSection['@id'])
            courses.append(aSection)
#             print(aSection)
#         print(tableIndex)
#         print(aCourseJsonObj)
#         break
        courses.append(aCourseJsonObj)
#     break
    courses.append(programJsonObj)

jsonObject['@graph'] = jsonObject['@graph']+courses

outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputObject['nextId'] = nextId
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('usc.jsonld','w')
f.write(outputFile)
f.close()


