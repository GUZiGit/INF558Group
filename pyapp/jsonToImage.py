import json
import subprocess


f = open('test.json')
jsonObj = json.load(f)

def getName(obj):
    if '@type' not in obj.keys():
        print(obj)
        return '' if '@id' not in obj.keys() else obj['@id']
    
    if obj['@type']=='ckb:Course':
        return obj['ckb:CourseName']
    if obj['@type']=='ckb:Section':
        return obj['ckb:sectionID']
    if obj['@type']=='ckb:Instructor':
        return obj['ckb:InstructorName']

def buildLinks(obj,rootName):
    linkAns = ''
    
#     if rootName=='ckb:Description':
#         return ''
    
    if type(obj) is list:
        for child in obj:
            linkAns += '<'+rootName+'>' +'->'+ '<'+getName(child)+'>' +';\n'
            linkAns += buildLinks(child,getName(child))
            
    elif type(obj) is dict:
        for childKey in obj.keys():
            
            if childKey in ['ckb:CourseName','ckb:InstructorName','ckb:sectionID','@type','@id','ckb:InstructorID','CourseID']:
                continue
            
            if type(obj[childKey]) is list:
                linkAns += '<'+rootName+'>' +'->'+  '<'+childKey+'>' +';\n'
                linkAns += buildLinks(obj[childKey],childKey)
            elif type(obj[childKey]) is str and childKey=='ckb:Description':
                linkAns += ''
            elif type(obj[childKey]) is str:
                linkAns += '<'+rootName+'>' +'->'+ '<'+obj[childKey]+'>' +'[label=<'+childKey+'>]'+';\n'
#                 linkAns += '<'+childKey+'>' +'->'+ '<'+obj[childKey]+'>' +';\n'
            elif type(obj[childKey]) is dict:
                linkAns += '<'+rootName+'>' +'->'+ '<'+getName(obj[childKey])+'>' +'[label=<'+childKey+'>]'+';\n'
                linkAns += buildLinks(obj[childKey],getName(obj[childKey]))
    else:
        print('wrong obj')
    
    return linkAns


f = open('temp.dot','w')
f.write('strict digraph tree {  ')
f.write(buildLinks(jsonObj,getName(jsonObj)))
f.write('}')
f.close()


subprocess.run(['dot','-Tpng','temp.dot','-o','temp.png', '-Gsize=18,19\!','-Gdpi=100'])

