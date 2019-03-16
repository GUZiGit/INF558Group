import scrapy
import sys

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
			yield scrapy.Request(url = url, callback = self.parse)

	def parse(self,response):
		content = response.body
		content = content.decode('utf-8')

		print(content)

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
