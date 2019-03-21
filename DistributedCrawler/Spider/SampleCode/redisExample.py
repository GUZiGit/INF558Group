import redis


port = 6379
hostName = '54.183.40.123'

__newUrlKey = 'NewUrl'
__crawledUrlKey = 'CrawledUrl'


r = redis.Redis(host=hostName,port=port)

# r = redis.Redis(host=hostName,port=port)

r.set('foo','bar')
print(r.get('foo').decode('utf-8'))

pipe = r.pipeline(transaction=False)
pipe.smembers(__newUrlKey)
pipe.delete(__newUrlKey)
result = pipe.execute()
print(type(result[0]))



print(result)
