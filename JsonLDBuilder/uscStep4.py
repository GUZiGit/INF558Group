import os
import sys
import json
from pyld import jsonld
from lxml.html.soupparser import fromstring
import re
import urllib
import PyPDF4
# response = urllib2.urlopen('http://www.example.com/')
# html = response.read()

folderDir = 'USC'
fileList = os.listdir(folderDir)

f = open('usc.jsonld')
jsonObject = json.load(f)
f.close()

nextId = jsonObject['nextId']


for obj in jsonObject['@graph']:
    if (obj['@type']=='ckb:Section') and ('ckb:Syllabus' in obj.keys()) and ('PDF'==obj['ckb:Syllabus']):
        tempPdfDir = 'USC/syllabus/'+obj['ckb:sectionID']+'.pdf'
        f = open(tempPdfDir,'rb')
        try:
            pdfReader = PyPDF4.PdfFileReader(f)
            m = re.findall(r'(?i)office hour[s]?[:]?[\s\n]*?([\d\w\-\.\,\:\t]+[\d]*)',pdfReader.getPage(0).extractText())
            if len(m)>0 and len(' '.join(m))>2:
#                 print(' '.join(m))
#                 print(tempPdfDir)
                obj['ckb:OfficeHour'] = ' '.join(m)
            m = re.findall(r'[e|E][-]?[m|M]ail[:]?[\s]*?([\w\.-]+@[\w\.-]+)',pdfReader.getPage(0).extractText())
            if len(m)>0:
                obj['ckb:email'] = m[0]
#                 print(m[0])
#                 print(tempPdfDir)
        except:
            continue



outputObject = jsonld.compact(jsonObject['@graph'],jsonObject['@context'])
outputObject['nextId'] = nextId
outputFile = json.dumps(outputObject,indent = 2)
# print(outputFile)

f=open('usc.jsonld','w')
f.write(outputFile)
f.close()
