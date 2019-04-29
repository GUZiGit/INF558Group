from kafka import KafkaProducer


kafkaHost = '18.144.51.15:9092'
enrollTopic = 'spiderEnroll'
topic = 'test3'
message = 'spiderName'


p = KafkaProducer(bootstrap_servers=[kafkaHost])


future = p.send(enrollTopic,message.encode('ascii'));


try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

