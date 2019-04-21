import scrapy
import sys
import json
from databackend import MongoBackend
from databackend import RedisBackend
import re

class LocalSpider(scrapy.Spider):
	name = 'spiderName'
	debugMode = False
	mongoBackend = MongoBackend()
	redisBackend = RedisBackend()

	def start_requests(self):
		urls = sys.argv[1]
		if self.debugMode:
			print('urls: '+urls)
		urls = urls.split('$')
		if self.debugMode:
			for url in urls:
				print('LocalSpider.start_requests(): '+url)
			print(urls)
		for url in urls:

			if self.debugMode:
				print('in Request: '+url)

			if url=="https://classes.usc.edu/term-20191/":
				yield scrapy.Request(url = url, callback = self.Hompage_parse, dont_filter = True)
			elif "https://classes.usc.edu/term-20191/class" in url:
				yield scrapy.Request(url=url,callback=self.Content_parse,dont_filter = True)
	def Hompage_parse(self,response):
		# content = response.body
		# content = content.decode('utf-8')

		if self.debugMode:
			print(response.body)

		f = open('USC/main.html','w')
		f.write(response.body.decode('utf-8'))
		f.close()

		# urlsForPush = []
		for courseURL in response.xpath('//ul[@id="sortable-classes"]/li'):
			URL=courseURL.xpath('a/@href').extract_first()
			
		# 	if debugMode:
		# 		print('new url: ' +URL)
		# 	urlsForPush.append(URL)

			yield scrapy.Request(url=URL,callback=self.Content_parse)


		# self.redisBackend.pushUrls(urlsForPush)

	def Content_parse(self,response):
		
		regex = re.compile('[^a-zA-Z0-9]')

		courseName = response.xpath('//div[@class="course-table"]/div').xpath('div/h3/a/text()').extract_first()

		f = open('USC/'+regex.sub('',courseName)+'.html','w')
		f.write(response.url+'\n')
		f.write(response.body.decode('utf-8'))
		f.close()

		# courseInfor={}
		# if response.status!=404:
		# 	Major=response.xpath('//h2[@class="dept-title"]/text()').extract_first()
		# 	if Major!= None and Major!="Not found":
		# 		courseInfor["Major"]=Major
		# 		courseInfor["class"]=[]
		# 		for course in response.xpath('//div[@class="course-table"]/div'):
		# 			courseAbbre=course.xpath('div/h3/a/strong/text()').extract_first()
		# 			courseName=course.xpath('div/h3/a/text()').extract_first()
		# 			catalogue=course.xpath('div[2]/div[@class="catalogue"]/text()').extract_first()
		# 			section=course.xpath('div[2]/table/tr[2]/td[1]/text()').extract_first()
		# 			Type=course.xpath('div[2]/table/tr[2]/td[3]/text()').extract_first()
		# 			day=course.xpath('div[2]/table/tr[2]/td[5]/text()').extract_first()
		# 			Instructor=course.xpath('div[2]/table/tr[2]/td[7]/a/text()').extract_first()
		# 			syllabus=course.xpath('div[2]/table/tr[2]/td[9]/a/@href').extract_first()
		# 			courseInfor["class"].append({
		# 				'courseAbbre':courseAbbre,
		# 				'courseName':courseName,
		# 				'catalogue':catalogue,
		# 				'section':section,
		# 				'Type':Type,
		# 				'day':day,
		# 				'Instructor':Instructor,
		# 				'syllabus':syllabus
		# 				})
		# # print(courseInfor)
		# self.mongoBackend.insertUSC(courseInfor)




		# 1. content, tag
		# 2. url, pdf, ...
		# 3. USC UCLA 

		# switch:

		# USC UCLA xxx






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
