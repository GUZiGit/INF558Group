from kafka import KafkaProducer
from kafka import KafkaConsumer
import os

class Spider:
	"""full implementation of spider"""

	kafkaHost = '18.144.51.15:9092'
	enrollTopic = 'spiderEnroll'
	channel = None

	debugMode = True

	def __init__(self,id):
		self.id = id;


	def enroll(self):
		# 1. send message to enroll
		# 2. try self topic, until success

		enrollMessage = self.id;

		p = KafkaProducer(bootstrap_servers=[self.kafkaHost])
		future = p.send(self.enrollTopic,enrollMessage.encode('ascii'))
		try:
			record_metadata = future.get(timeout=10)
		except KafkaError:
			# log.exception()
			print('enroll() Error: send enroll message Error.')
			return False



		self.channel = KafkaConsumer(self.id,bootstrap_servers=[self.kafkaHost])

		print("Wait for enroll confirm.")
		for message in self.channel:
			if self.debugMode:
				print('enroll():' + message.value.decode('utf-8'))
			if message.value.decode('utf-8')==self.id:
				return True

	def processMessage(self):
		print("Spider "+self.id+" start processMessage()")
		for message in self.channel:
			if self.debugMode:
				print('processMessage(): '+message.value.decode('utf-8'))
			if message.value.decode('utf-8')=='quit':
				exit()
			else:
				self.crawl(message.value.decode('utf-8'))

	def crawl(self,message):

		# message format: url$url$url...

		if self.debugMode:
			print('crawl(): '+message)
		os.system('python3 runLocalSpider.py '+ message)


	def run(self):
		# 1. enroll()
		# 2. wait for message
		# 3. execute command
		self.enroll()
		self.processMessage()


def main():
	s = Spider('spiderTest1')
	s.run()



if __name__ == '__main__':
	main()




