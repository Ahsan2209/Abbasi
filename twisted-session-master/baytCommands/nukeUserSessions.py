from sessions_fix import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer, reactor
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
class nukeUserSessions(bayt_command):
	CMDName  = 'nukeUserSessions'

	def end(self, *args):
		self._writeBack(NO_ERROR)
		self.SetDone()
	
	@defer.inlineCallbacks
	def postWrite(self):
		#Allow python genrator to work, even if there is no internal deferred got fired. 
		def empty():
			pass
		yield defer.maybeDeferred(empty)
		#objects to be used
		vars = self._getVarsList()
		user_id = vars.get('user_id')
		if user_id is None or user_id == "":
					self._protocol.quickResponse(MISSING_VARS)
					self.SetDone()
					defer.returnValue(None)	
		self.sessionCache = SessionsRedis()
		d = self.sessionCache.deleteUserSessions(user_id)
		d1 = d.addCallback(self.end)
		reactor.callLater(0, d1.callback,"")
		
		defer.returnValue(None)	