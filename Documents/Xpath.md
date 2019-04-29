## UCLA
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