from kafka import KafkaConsumer

k = KafkaConsumer('notexist',bootstrap_servers=['18.144.51.15:9092'])
for m in k:
	print(m.value.decode('utf-8'))
