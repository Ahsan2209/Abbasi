from Sessions import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
class LogoutProcess(bayt_command):
	CMDName  = 'LogoutProcess'

	@defer.inlineCallbacks
	def postWrite(self):
		#Allow python genrator to work, even if there is no internal deferred got fired. 
		def empty():
			pass
		yield defer.maybeDeferred(empty)
		#objects to be used
		vars = self._getVarsList()
		session_id = vars.get('session_id')	
		session_type = vars.get('session_type')
		user_id = vars.get('user_id')
		bcc_id = vars.get('bcc_id')
		browser_id = vars.get('browser_id')
		if session_id == "" or session_type == ""  or \
				user_id == "" or bcc_id == "" or browser_id == "":
					self._protocol.quickResponse(MISSING_VARS)
					self.SetDone()
					defer.returnValue(None)	
		
		
		
		
		#Load all cookies:
		sessionCache = SessionsRedis()
		cookies = sessionsCookies()
		response = SessionResponse.responseFromSessionCache( \
				"2","","0", \
				sessionCache,DUMMY_SESSION["context_time"], DUMMY_SESSION["life_sapn"], \
				True,"","0", \
				True,"", \
				False,browser_id)
		self._writeBack(response)
		
		res= yield sessionCache.getSessionInfo(session_id,session_type,bcc_id,user_id)
		if not res:
			self.SetDone()
			defer.returnValue(None)	
		
		yield sessionCache.delete()
		self.SetDone()
		defer.returnValue(None)	