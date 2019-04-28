import requests
import json
import elasticsearch
import elasticsearch_dsl
import subprocess
from PIL import Image, ImageTk
from tkinter import Tk, Label, Listbox, StringVar,Entry, Button,NW, Text, Scrollbar
import tkinter

# subprocess.run(['rm','temp.png'])

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])

root = Tk()

w, h = root.maxsize()
root.geometry("{}x{}".format(w, h)) 

# sb = Scrollbar(root)
# sb.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# sb2 = Scrollbar(root)
# sb2.pack(side=tkinter.BOTTOM, fill=tkinter.X)

# root.geometry('900x600')

baseLabel = Label(root,text='Breath Search by')
baseLabel.place(x=0,y=3,anchor=NW)

searchType = Listbox(root,selectmod='BROWSE')
searchType.insert(0,'id','Program','Course','Section','Instructor')
searchType.select_set(0)
searchType.place(x=120,y=3,anchor=NW)

imageLabel = Label(root,width=1800,height=1000)

# img1 = ImageTk.PhotoImage(file='test.png')
# imageLabel.config(image=img1)
# imageLabel.image = img1 

imageLabel.place(x=3,y=300)


en = Entry(root)
en.place(x=300,y=3,anchor=NW)

def pressSubmit():
#     outcome.set( en.get()+'\n')
#     print(searchType.curselection())
    print(en.get())
    print(searchType.get(searchType.curselection()))
    
#     try:
#         t = searchType.get(searchType.curselection())
#         t = en.get()
#     except:
#         return
    searchField = searchType.get(searchType.curselection())
    searchKeyword = en.get()
    
    basicBody = {
      'query': {
          'bool':{
              'must':[
                  {'match':{}},
                  {'match':{}}
              ]
          }
      }
    }
    
    if searchField=='Program':
        basicBody['query']['bool']['must'][0]['match']={'@type': 'ckb:Course'}
        basicBody['query']['bool']['must'][1]['match']={'ckb:ProgramName': searchKeyword}
        
    elif  searchField=='Course':
        basicBody['query']['bool']['must'][0]['match']={'@type': 'ckb:Course'}
        basicBody['query']['bool']['must'][1]['match']={'ckb:CourseName': searchKeyword}
    elif  searchField=='Section':
        basicBody['query']['bool']['must'][0]['match']={'@type': 'ckb:Section'}
        basicBody['query']['bool']['must'][1]['match']={'@id': searchKeyword}
    elif  searchField =='Instructor':
        basicBody['query']['bool']['must'][0]['match']={'@type': 'ckb:Instructor'}
        basicBody['query']['bool']['must'][1]['match']={'ckb:InstructorName': searchKeyword}
    elif  searchField =='id':
        basicBody['query']['bool']['must'][0]['match']={'@id': '_:'+searchKeyword}
        basicBody['query']['bool']['must'][1]['match']={'@id': '_:'+searchKeyword}
    else:
        return
    
    print(basicBody)
    searchResult = es.search(index='uscfinal',size=1000, body=basicBody)
    print()
    objList = []
    for r in searchResult['hits']['hits']:
#         print(r['_source'])
        objList.append(r['_source'])
    
    f = open('test.json','w')
    f.write(json.dumps(objList))
    f.close()
#     python3 .\json_viewer.py .\test.json
    process = subprocess.Popen(['python3', 'json_viewer.py','test.json'])
    
#     print(searchResult['hits']['hits'])
#     outcome.set(searchResult['hits']['hits'])
#     localAns = ''
#     for aSearchResult in searchResult['hits']['hits']:
#         for k in aSearchResult.keys():
#             localAns +=str( aSearchResult[k])
#             localAns += '\n'
#     outcome.set(localAns)

bu = Button(root,text='submit',command=pressSubmit)
bu.place(x=450,y=3,anchor=NW)


depthBaseLabel = Label(root,text='Depth Search by')
depthBaseLabel.place(x=0,y=300,anchor=NW)

depthSearchType = Listbox(root,selectmod='BROWSE')
depthSearchType.insert(0,'Course','Section','Instructor')
depthSearchType.select_set(0)
depthSearchType.place(x=120,y=300,anchor=NW)

depthEn = Entry(root)
depthEn.place(x=300,y=300,anchor=NW)


def depthSubmit():
    print(depthEn.get())
    print(depthSearchType.get(depthSearchType.curselection()))
    
#     try:
#         t = searchType.get(searchType.curselection())
#         t = en.get()
#     except:
#         return
    searchField = depthSearchType.get(depthSearchType.curselection())
    searchKeyword = depthEn.get()
    
    basicBody = {
      'query': {
          'bool':{
              'must':[
                  {'match':{}},
                  {'match':{}}
              ]
          }
      }
    }
    
    outputObj = {}
    
    if  searchField=='Course':
        basicBody['query']['bool']['must'][0]['match']={'@type': 'ckb:Course'}
        basicBody['query']['bool']['must'][1]['match']={'ckb:CourseName': searchKeyword}
        print(basicBody)
        searchResult = es.search(index='uscfinal',size=2, body=basicBody)
        courseObj = searchResult['hits']['hits'][0]['_source']
        print(courseObj)
        
        courseObj['sectionObjects'] = []

        if 'ckb:sections' in courseObj.keys():
            if type(courseObj['ckb:sections'])==list:
                for tempSectionID in courseObj['ckb:sections']:
                    basicBody['query']['bool']['must'][0]['match']={'@id': tempSectionID}
                    basicBody['query']['bool']['must'][1]['match']={'@id': tempSectionID}
                    print(basicBody)
                    searchResult = es.search(index='uscfinal',size=2, body=basicBody)
                    tempSectionObj = searchResult['hits']['hits'][0]['_source']
                    if 'ckb:InstructorID' in tempSectionObj.keys():
                        basicBody['query']['bool']['must'][0]['match']={'@id': tempSectionObj['ckb:InstructorID']}
                        basicBody['query']['bool']['must'][1]['match']={'@id':tempSectionObj['ckb:InstructorID']}
                        print(basicBody)
                        searchResult = es.search(index='uscfinal',size=2, body=basicBody)
                        tempSectionObj['Instructor'] = searchResult['hits']['hits'][0]['_source']

                    courseObj['sectionObjects'].append(tempSectionObj)
            else:
                basicBody['query']['bool']['must'][0]['match']={'@id': courseObj['ckb:sections']}
                basicBody['query']['bool']['must'][1]['match']={'@id': courseObj['ckb:sections']}
                print(basicBody)
                searchResult = es.search(index='uscfinal',size=2, body=basicBody)
                tempSectionObj = searchResult['hits']['hits'][0]['_source']
                if 'ckb:InstructorID' in tempSectionObj.keys():
                    basicBody['query']['bool']['must'][0]['match']={'@id': tempSectionObj['ckb:InstructorID']}
                    basicBody['query']['bool']['must'][1]['match']={'@id':tempSectionObj['ckb:InstructorID']}
                    print(basicBody)
                    searchResult = es.search(index='uscfinal',size=2, body=basicBody)
                    tempSectionObj['Instructor'] = searchResult['hits']['hits'][0]['_source']

                courseObj['sectionObjects'].append(tempSectionObj)
        
            courseObj['ckb:sections'] = courseObj['sectionObjects']
            del courseObj['sectionObjects']

        outputObj = courseObj

        
    elif  searchField=='Section':
        basicBody['query']['bool']['must'][0]['match'] = {'@type':'ckb:Course'}
        basicBody['query']['bool']['must'][1]['match'] = {'ckb:sections': '_:'+searchKeyword}
        print(basicBody)
        searchResult = es.search(index='uscfinal',size=2, body=basicBody)
        courseObj = searchResult['hits']['hits'][0]['_source']
        
        basicBody['query']['bool']['must'][0]['match'] = {'@type': 'ckb:Section'}
        basicBody['query']['bool']['must'][1]['match']= {'@id': '_:'+searchKeyword}
        print(basicBody)
        searchResult2 = es.search(index='uscfinal',size=2, body=basicBody)
        sectionObj = searchResult2['hits']['hits'][0]['_source']
        
        courseObj['ckb:sections'] = sectionObj
        
        if "ckb:InstructorID" in sectionObj.keys():
            basicBody['query']['bool']['must'][0]['match']= {'@id': sectionObj['ckb:InstructorID']}
            basicBody['query']['bool']['must'][1]['match']= {'@id': sectionObj['ckb:InstructorID']}
            print(basicBody)
            searchResult3 = es.search(index='uscfinal',size=2, body=basicBody)
            instructorObj = searchResult3['hits']['hits'][0]['_source']
            
            sectionObj['ckb:InstructorID'] = instructorObj
        
        outputObj = courseObj
        
#         basicBody['query']['bool']['must'][0]['match']['@type'] = 'ckb:Section'
#         basicBody['query']['bool']['must'][1]['match']['@id']= '_:'+searchKeyword
        
    elif  searchField =='Instructor':
        basicBody['query']['bool']['must'][0]['match'] = {'@type':'ckb:Instructor'}
        basicBody['query']['bool']['must'][1]['match'] = {'ckb:InstructorName': searchKeyword}
        print(basicBody)
        searchResult = es.search(index='uscfinal',size=2, body=basicBody)
        instructorObj = searchResult['hits']['hits'][0]['_source']
        instructorObj['sections'] = []
        
        basicBody['query']['bool']['must'][0]['match'] = {'@type':'ckb:Section'}
        basicBody['query']['bool']['must'][1]['match'] = {'ckb:InstructorID': instructorObj['@id']}
        print(basicBody)
        searchResult = es.search(index='uscfinal',size=1000, body=basicBody)
#         tempSectionIDList = []
        for tempSection in searchResult['hits']['hits']:
            instructorObj['sections'].append(tempSection['_source'])
#             tempSectionIDList.append(tempSection['_source']['@id'])
        
#         tempCourseIDList = []
        
        for tempSection in instructorObj['sections']:
            basicBody['query']['bool']['must'][0]['match'] = {'@type':'ckb:Course'}
            basicBody['query']['bool']['must'][1]['match'] = {'ckb:sections':tempSection['@id']}
            print(basicBody)
            searchResult = es.search(index='uscfinal',size=2, body=basicBody)
            tempSection['CourseID'] = searchResult['hits']['hits'][0]['_source']['@id']
            tempSection['CourseName'] = searchResult['hits']['hits'][0]['_source']['ckb:CourseName']
            print(basicBody)
#             if tempCourseID not in tempCourseIDList:
#                 tempCourseIDList.append(tempCourseID)
        
        outputObj = instructorObj
        
        
#     elif  searchField =='id':
#         basicBody['query']['bool']['must'][0]['match'] = {'@id':searchKeyword}
#         basicBody['query']['bool']['must'][1]['match'] = {'@id':searchKeyword}
        
        
        
    else:
        return
    
#     print(basicBody)
#     searchResult = es.search(index='uscfinal',size=1000, body=basicBody)
#     print()
#     objList = []
#     for r in searchResult['hits']['hits']:
# #         print(r['_source'])
#         objList.append(r['_source'])
    
    
    
    f = open('test.json','w')
    f.write(json.dumps(outputObj))
    f.close()
#     python3 .\json_viewer.py .\test.json
    subprocess.run(['python3','jsonToImage.py'])
    process = subprocess.Popen(['python3', 'json_viewer.py','test.json'])

    img1 = ImageTk.PhotoImage(file='temp.png')
    imageLabel.config(image=img1)
    imageLabel.image = img1 



depthBu = Button(root,text='submit',command=depthSubmit)
depthBu.place(x=450,y=300,anchor=NW)


root.mainloop()
