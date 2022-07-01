from datetime import datetime
from log.log import *
from twisted.internet import defer
class bayt_command:
	CMDName = None
	def preWrite(self):
		
		pass
	def postWrite(self):
		pass
	def setCommandsDependency(self,protocol,listVar):
		self._listVar = listVar
		self._protocol = protocol
	def _writeBack(self,msg,loseConnection=False):
		self._protocol.writeLine(msg)
		if loseConnection is True:
			self._protocol.transport.loseConnection()
	def _quickResponse(self,msg):
		self._protocol.quickResponse(msg)
	def _getVarsList(self):
		return self._listVar
	def getRevision(self):
		return '1.0'
	
	def SetDone(self):
		self._protocol._status = 0
		if self._protocol.connected and self._protocol._closeAtExit:
			self._protocol.transport.loseConnection()
		total_time =  datetime.now() - self._protocol._start_time
		if total_time.seconds > 29:
			bayt_log.logError("time","more than 30 seconds :\n" , "")	 
