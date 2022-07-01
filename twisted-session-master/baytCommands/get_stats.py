from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from utils.commandsClient.ERRORS import *

class get_stats(bayt_command):
	CMDName  = 'get_stats'
	def postWrite(self):
		#excecute_insert_transaction
		vars = self._getVarsList()
		res = {}
		res['totalConnections'] = self._protocol.factory.getConnectionsCount()
		res['totalAccess'] = self._protocol.factory.getLogCount()
		res['startTime'] =  self._protocol.factory.getStartTime()
		self._writeBack(res)
		self.SetDone()