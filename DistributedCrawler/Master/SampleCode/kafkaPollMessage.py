from kafka import KafkaConsumer, KafkaClient, TopicPartition
from time import sleep

# client = KafkaClient('18.144.51.15:9092')
# topic_partition_ids = client.get_partition_ids_for_topic('newUrl')

# print(topic_partition_ids)

# [TopicPartition('foobar', 2)]

k = KafkaConsumer('newUrl',bootstrap_servers=['18.144.51.15:9092'],group_id='another')
# 
# k
# k.assign(TopicPartition('newUrl',0))



# k.seek_to_beginning()

# print(k.end_offsets())

# sleep(5)

print(k.poll())


sleep(8)


msg = k.poll()

# print(msg_pack)
for aKey in msg.keys():
    for localMessage in msg[aKey]:
        print(localMessage.value.decode('utf-8'))

# for tp, messages in msg_pack.items():
# message value and key are raw bytes -- decode if necessary!
# e.g., for unicode: `message.value.decode('utf-8')`
	# print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
	# 	messages.offset, messages.key,
	# 	messages.value))

# for m in k:
# 	print(m.value.decode('utf-8'))



# from kafka import KafkaConsumer

# k = KafkaConsumer('newUrl',bootstrap_servers=['18.144.51.15:9092'])
# for m in k:
# 	print(m.value.decode('utf-8'))

