from Sessions import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
class checkUserLogged(bayt_command):
	CMDName  = 'checkUserLogged'

	@defer.inlineCallbacks
	def postWrite(self):
		#Allow python genrator to work, even if there is no internal deferred got fired. 
		def empty():
			pass
		yield defer.maybeDeferred(empty)
		#objects to be used
		vars = self._getVarsList()
		session_id = vars.get('session_id')	
		
		if session_id == "":
					self._protocol.quickResponse(MISSING_VARS)
					self.SetDone()
					defer.returnValue(None)	
		
		
		
		info= yield SessionsRedis.get_simpleSessionInfo(session_id)
		if info.get("user_id") is None or info.get("user_id") == "":
			#If the session loading returns false, then that means it got expired....
			self._writeBack("0")
			self.SetDone()
			defer.returnValue(None)	
		self._writeBack( info["user_id"])
		self.SetDone()
		defer.returnValue(None)	
		
		
		
		
		