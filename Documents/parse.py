from lxml import html, etree
import json
import os
path = 'CRAWLED_DIR/'
fileList = os.listdir(path)
output_dir=".//reslut"
if not os.path.exists(output_dir):
          os.makedirs(output_dir)
for i in fileList:
	myfile=open(os.path.join('CRAWLED_DIR/'+ i), 'r')
	data=myfile.read()
	tree=html.fromstring(data)
	datajson={}
	subject=tree.xpath('//div[@class="page-header"]//span/text()')
	datajson["subject"]=subject[0]
	datajson["courses"]=[]
	for i in tree.xpath('//div[@class="tab-pane"]/ul/li/div'):
			numberAtitle=i.xpath('h3/text()')
			unit=i.xpath('p[1]/text()')
			description=i.xpath('p[2]/text()')
			if not description:
				description=""
			else:
				description=description[0]
			datajson["courses"].append({
				'course number & title': numberAtitle[0],
				'Number of unit': unit[0],
				'Course description': description
				})
	if "/" in subject[0]:
		subject[0]=subject[0].replace("/"," ")
	file=subject[0]+'.json'
	with open(output_dir+"/"+file, 'w') as outfile:  
	    json.dump(datajson, outfile)
