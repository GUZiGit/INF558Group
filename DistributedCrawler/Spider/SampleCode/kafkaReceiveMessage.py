from kafka import KafkaConsumer

k = KafkaConsumer('newUrl',bootstrap_servers=['18.144.51.15:9092'],group_id='default')
for m in k:
	print(m.value.decode('utf-8'))

