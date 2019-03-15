# full implementation of spider

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

 		




