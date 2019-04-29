import pymongo
import redis

class RedisBackend:

	__newUrlKey = 'newUrl'
	__crawledUrlKey = 'CrawledUrl'


	__port = 6379
	__hostName = '54.183.40.123'

	redisOperator = redis.Redis(host=__hostName,port=__port)
	pub = redisOperator.pubsub()

	def __init__(self):
		pass

	# this function only serve for spider
	def pushUrls(self,urls):
		# urls: list of url
		for url in urls:
			# self.redisOperator.sadd(self.__newUrlKey,url)
			self.redisOperator.publish(self.__newUrlKey,url)

	# this function only seve for master
	def pullUrls(self):

		# pipeline as multi, transaction = false
		pipe = self.redisOperator.pipeline(transaction=False)
		pipe.smembers(self.__newUrlKey)
		pipe.delete(self.__newUrlKey)
		urls = pipe.execute()[0]
		urls = list(map(lambda u: u.decode('utf-8'),urls))
		return urls


class MongoBackend:

	def __init__(self):
		self.myClient = pymongo.MongoClient('mongodb://54.193.51.217')


	# insert one json object in USC collection
	def insertUSC(self, content):
		crawlerDB = self.myClient['crawler']
		usc = crawlerDB['USC']
		usc.insert_one(content)


