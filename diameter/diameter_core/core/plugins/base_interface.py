##
## @brief      Base class for interfaces' inheritance
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##
class BaseInterface(object):
	def __init__(self):
		pass
	
	##
	## @brief      Load a configuration file for the interface
	##
	## @param      self  refers to the class itself
	## @param      conf  the configuration file
	##
	def loadConfig(self, conf):
		if len(conf) == 0 or conf is None:
			raise Exception("Missing configfile")
		self.conf = conf
	
	##
	## @brief      Abstract: A private function to generate a specific message
	##
	## @param      self  refers to the class itself
	##
	def __generateMessage(self):
		pass
	
	##
	## @brief      Abstract: generate all the messages of the interface
	##
	## @param      self  refers to the class itself
	##
	def generateMessages(self):
		pass
		