import scrapy
import sys
import json
class LocalSpider(scrapy.Spider):
	name = 'spiderName'
	debugMode = False

	def start_requests(self):
		urls = sys.argv[1]
		if self.debugMode:
			print('urls: '+urls)
		urls = urls.split('$')
		if self.debugMode:
			for url in urls:
				print('LocalSpider.start_requests(): '+url)
		for url in urls:
			if url=="https://classes.usc.edu/term-20191/":
				yield scrapy.Request(url = url, callback = self.Hompage_parse)
			elif "https://classes.usc.edu/term-20191/class" in url:
				yield scrapy.Request(url=url,callback=self.Content_parse)
	def Hompage_parse(self,response):
		# content = response.body
		# content = content.decode('utf-8')
		for courseURL in response.xpath('//ul[@id="sortable-classes"]/li'):
			URL=courseURL.xpath('a/@href').extract_first()
			yield scrapy.Request(url=URL,callback=self.start_requests)
	def Content_parse(self,response): ß
		courseInfor={}
		if response.status!=404:
			Major=response.xpath('//h2[@class="dept-title"]/text()').extract_first()
			if Major!= None and Major!="Not found":
				courseInfor["Major"]=Major
				courseInfor["class"]=[]
				for course in response.xpath('//div[@class="course-table"]/div'):
					courseAbbre=course.xpath('div/h3/a/strong/text()').extract_first()
					courseName=course.xpath('div/h3/a/text()').extract_first()
					catalogue=course.xpath('div[2]/div[@class="catalogue"]/text()').extract_first()
					section=course.xpath('div[2]/table/tr[2]/td[1]/text()').extract_first()
					Type=course.xpath('div[2]/table/tr[2]/td[3]/text()').extract_first()
					day=course.xpath('div[2]/table/tr[2]/td[5]/text()').extract_first()
					Instructor=course.xpath('div[2]/table/tr[2]/td[7]/a/text()').extract_first()
					syllabus=course.xpath('div[2]/table/tr[2]/td[9]/a/@href').extract_first()
					courseInfor["class"].append({
						'courseAbbre':courseAbbre,
						'courseName':courseName,
						'catalogue':catalogue,
						'section':section,
						'Type':Type,
						'day':day,
						'Instructor':Instructor,
						'syllabus':syllabus
						})
		print(courseInfor)




		# 1. content, tag
		# 2. url, pdf, ...
		# 3. USC UCLA 

		# switch:

		# USC UCLA xxx



		# xpath...
		# tag

		# save somewhere

		# save urls in redis
		# save key value pares in mongoDB
