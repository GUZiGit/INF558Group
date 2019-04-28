

class Master:
	"""Full implementation of Master class"""
	def __init__(self):

		self.spiderEnrollChannel = KafkaConsumer('spiderEnroll',bootstrap_servers=['18.144.51.15:9092'])
		
		
	def run(self):

		# link to kafka


		# load config


		# url checks


		# spider checks


		# fetch all spiders


		# fetch all urls

			# fetch and delete


		# prepare jobs to send

			# check timestamp - now last time

			# preapare number of urls for each domains

			# wait unit second

		# send jobs


		pass



