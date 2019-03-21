import redis

class RedisBackend:

	__newUrlKey = 'NewUrl'
	__crawledUrlKey = 'CrawledUrl'


	__port = 6379
	__hostName = '54.183.40.123'

	redisOperator = redis.Redis(host=__hostName,port=__port)

	def __init__(self):
		pass

	# this function only serve for spider
	def pushUrls(self,urls):
		# urls: list of url
		for url in urls:
			self.redisOperator.sadd(self.__newUrlKey,url)

	# this function only seve for master
	def pullUrls(self):

		# pipeline as multi, transaction = false
		pipe = self.redisOperator.pipeline(transaction=False)
		pipe.smembers(self.__newUrlKey)
		pipe.delete(self.__newUrlKey)
		urls = pipe.execute()[0]
		urls = list(map(lambda u: u.decode('utf-8'),urls))
		return urls

