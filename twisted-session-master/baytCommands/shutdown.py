from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from utils.commandsClient.ERRORS import *
from twisted.internet.protocol import Factory

def closeOnDone(*args,**kwargs):
	
	baytFactory = kwargs['baytFactory']
	if baytFactory.checkAllDone():
		baytFactory.reactor.stop()
	else:
		baytFactory.reactor.callLater(1,closeOnDone,baytFactory = baytFactory)
 
class shutdown(bayt_command):
	CMDName  = 'shutdown'
	@defer.inlineCallbacks
	def postWrite(self):
		import os
		pid = os.getpid()
		factory = self._protocol.factory
		self._quickResponse(str(pid))
		yield self._protocol.factory.iis.stopListening()
		for protocol in factory._protocols:
			if protocol.isActive() == 1:
				protocol.closeConnectionAtExit()
			else:
				protocol.loseConnection()		   #print	 
		closeOnDone(baytFactory = factory)
		self.SetDone()
		