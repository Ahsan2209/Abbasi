from commandsProtocolV2 import commandsProtocol
from twisted.internet.protocol import Factory
from twisted.internet import defer

class baytFactory(Factory):
	protocol = commandsProtocol
	def __init__(self, maxConnections,user,password,myReactor):
		self.maxCon = maxConnections
		self.connectionCount = 0	
		self.user = user
		self.password = password
		self.logCount = 0
		self._protocols = []
		self.reactor = myReactor
		self._stopDone = False
		self._cache = {}
		
		from time import gmtime, strftime
		self.StartTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	def increaseCount(self):
		self.connectionCount += 1
		if self.maxCon != 0 and self.connectionCount > self.maxCon:
			return True
		else:
			return False
	def getStartTime(self):
		return self.StartTime
		
	def increaseLogCount(self):
		self.logCount +=1
	def getLogCount(self):
		return self.logCount
	def decreaseCount(self):
		self.connectionCount -= 1
	
	def getConnectionsCount(self):
		return self.connectionCount   
	def getCacheValue(self,key_name):
		return self._cache.get(key_name)   
	
	def setCacheValue(self,key_name,value):
		self._cache[key_name] = value
	def get_userName(self):
		return self.user
	def get_password(self):
		return self.password
	
	def checkAllDone(self):
		if self.connectionCount > 0 :
			return False
		return True
	
		
		
