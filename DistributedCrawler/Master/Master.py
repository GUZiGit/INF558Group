from kafka import KafkaConsumer,KafkaProducer
from random import randint


class Master:
	"""Full implementation of Master class"""
	def __init__(self):

		self.spiderEnrollChannel = KafkaConsumer('spiderEnroll',bootstrap_servers=['18.144.51.15:9092'],group_id='unique')
		self.urlChannel = KafkaConsumer('newUrl',bootstrap_servers=['18.144.51.15:9092'],group_id='unique')
		self.urls = []
		self.spiders = []

		# self.lastTimeSend =
 

	def loadConfig(self):

		self.domainPriority = [] # a list of domain ordered by priority
		self.crawlSpeed = 3  #  per second for each spider
		
	
	def checkUrl(self):

		if len(self.urls) > 0:
			return

		else:
			print('wait for url')
			for m in self.urlChannel:
				self.urls.append(m.value.decode('utf-8'))
				# print(m.value.decode('utf-8'))
				print('load url: '+m.value.decode('utf-8'))
				break

	def checkSpider(self):
		if len(self.spiders) > 0:
			return

		else:
			print('wait for spider')
			for m in self.spiderEnrollChannel:
				self.spiders.append(m.value.decode('utf-8'))
				# print(m.value.decode('utf-8'))
				print('load spider: '+m.value.decode('utf-8'))
				break

	def fetchAllSpiders(self):
		print("fetch all spiders")
		msg = self.spiderEnrollChannel.poll()

		for aKey in msg.keys():
			for localMessage in msg[aKey]:
				print(localMessage.value.decode('utf-8'))
				self.spiders.append(localMessage.value.decode('utf-8'))
		print('done')
		print(self.spiders)

	def fetchAllUrls(self):

		print('fetch all urls')
		msg = self.urlChannel.poll()

		for aKey in msg.keys():
			for localMessage in msg[aKey]:
				print(localMessage.value.decode('utf-8'))
				self.urls.append(localMessage.value.decode('utf-8'))
		print('done')
		print(self.urls)

	def sendUrl(self,url):
		spiderIndex = randint(0,len(spiders))
		nextSpider = self.spiders[spiderIndex]
		print('send url: '+url + " to "+nextSpider)

		kafkaHost = '18.144.51.15:9092'

		p = KafkaProducer(bootstrap_servers=[kafkaHost])

		future = p.send(nextSpider,url.encode('ascii'));

		try:
		    record_metadata = future.get(timeout=10)
		except KafkaError:
		    # Decide what to do if produce request failed...
		    log.exception()
		    print("send error")
		    

		# Successful result returns assigned partition and offset
		# print (record_metadata.topic)
		# print (record_metadata.partition)
		# print (record_metadata.offset)

	
	def run(self):

		self.loadConfig()

		while True:

			# load config or predefined here
			

			# url checks
			self.checkUrl()

			# spider checks
			self.checkSpider()

			# fetch all spiders
			self.fetchAllSpiders()

			# fetch all urls
			self.fetchAllUrls()
				# fetch and delete

			for url in self.urls:
				self.sendUrl(url)



			# prepare jobs to send

				# check timestamp - now last time

				# preapare number of urls for each domains

				# wait unit second

			# send jobs


			# pass

def main():
	master = Master()
	master.run()


if __name__ == '__main__':
	main()	
