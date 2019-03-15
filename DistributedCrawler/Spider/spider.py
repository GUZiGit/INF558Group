from kafka import KafkaProducer


class Spider:
 	"""full implementation of spider"""

 	kafkaHost = '18.144.51.15:9092'
 	enrollTopic = 'spiderEnroll'
 	# enrollConfirmTopic = 'spiderConfirm'

 	def __init__(self,id):
 		self.id = id;


 	def enroll(self):
 		# 1. send message to enroll
 		# 2. try self topic, until success

 		enrollMessage = self.id;

 		p = KafkaProducer(bootstrap_servers=[kafkaHost])
 		future = p.send(topic,enrollMessage.encode('ascii'));
 		try:
    		record_metadata = future.get(timeout=10)
		except KafkaError:
    		# log.exception()
    		print('enroll() Error: send enroll message Error.')
    		return False

    	c = KafkaConsumer(self.id,bootstrap_servers=[kafkaHost])

    	print("Wait for enroll confirm.")
    	for message in c:
			print(m.value.decode('utf-8'))
			if message.value.decode('utf-8')==self.id:
				return True


    






