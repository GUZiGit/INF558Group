import redis
from kafka import KafkaProducer

port = 6379
hostName = '54.183.40.123'



kafkaHost = '18.144.51.15:9092'
# enrollTopic = 'newUrls'
topic = 'newUrl'
message = 'send message test'
p = KafkaProducer(bootstrap_servers=[kafkaHost])

r = redis.Redis(host=hostName,port=port)


sub = r.pubsub()
sub.subscribe('newUrl')

for item in sub.listen():
	# print(item)
	bData = item['data']
	if item['type']=="subscribe":
		print(bData)
	if item['type']=="message":
		print(bData.decode('utf-8'))
		url = bData.decode('utf-8')
		future = p.send(topic,url.encode('ascii'));
		try:
			record_metadata = future.get(timeout=10)
		except KafkaError:
			# Decide what to do if produce request failed...
			log.exception()

















    
