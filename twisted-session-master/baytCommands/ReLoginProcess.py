from Sessions import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
class ReLoginProcess(bayt_command):
	CMDName  = 'ReLoginProcess'

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
		browser_info = vars.get('browser_info')			
		
	
		if session_id == "" or session_type == "" or browser_id == ""\
				or user_id == "" or bcc_id == "":
					self._protocol.quickResponse(MISSING_VARS)
					self.SetDone()
					defer.returnValue(None)	
		
		
		
		
		sessionCache = SessionsRedis()
		cookies = sessionsCookies()
		res= yield sessionCache.getSessionInfo(session_id,session_type,bcc_id,user_id)
		if not res or sessionCache.SessionInfo["is_permenant"] != "1":
			#If the session loading returns false, then that means it got expired....
			cookies.cookieSessionInfo["browser_id"] = browser_id
			response = yield DummySession(cookies,browser_info,bcc_id,new_browser_id=False)
			self._writeBack(response)
			self.SetDone()
			defer.returnValue(None)		
		sessionCache.SessionInfo["xsrf_token"] =  random_string_generator(6)
		sessionCache.SessionInfo["secure_token"] =  random_string_generator(6)
		sessionCache.SessionInfo["authenticate_time"] = str(now_time())
		sessionCache.SessionInfo["MSESID_to_BSESINFO"] = str(random.randrange(0,99))
		yield sessionCache.autoSave(update_BSESINFO=True)
		
		life_sapn = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["Permenant_life_sapn"]
		context_time = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["Permenant_context_time"]

		
		cookies.load_browserid_fromRedis(sessionCache)
		cookies.load_BSESINFO_fromRedis(sessionCache)
		cookies.load_MSESID_fromRedis(sessionCache)
		cookies.build_MSESID_cookie()
		cookies.build_BSESINFO_cookie()
		cookies.build_browserid_cookie()		
 
		response = SessionResponse.responseFromSessionCache( \
				2,"","0", \
				sessionCache,context_time,life_sapn, \
				False,cookies.MSESID_generated_cookie,sessionCache.SessionInfo["is_permenant"], \
				True,cookies.BSESINFO_generated_cookie, \
				False,cookies.browser_id_generated_cookie)	
		
		#FORCE allow_multi_bcc
		#redis_instance2
		self._writeBack(response)
			
		self.SetDone()
		defer.returnValue(None)	
		
		
		
		
		