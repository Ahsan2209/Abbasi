from utils.commandsClient.baytCommand import bayt_command
from sessions_fix import *
from twisted.internet import defer
from log.log import *
from utils.commandsClient.ERRORS import *

class get_seq_count(bayt_command):
	CMDName  = 'get_seq_count'
	@defer.inlineCallbacks
	def postWrite(self):
		#excecute_insert_transaction
		vars = self._getVarsList()
		res = {}
		res = yield sessionsSequences.sessionID_get()
		self._writeBack(res)
		self.SetDone()
		
