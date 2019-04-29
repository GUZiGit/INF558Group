import redis

port = 6379
hostName = '54.183.40.123'


r = redis.Redis(host=hostName,port=port)


sub = r.pubsub()
# sub.subscribe('notexist')

# for item in sub.listen():
# 	# print(item)
# 	bData = item['data']
# 	if item['type']=="subscribe":
# 		print(bData)
# 	if item['type']=="message":
# 		print(bData.decode('utf-8'))

r.publish('notexist','uxrl')

