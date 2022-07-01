from Sessions import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
class refreshProcess(bayt_command):
	CMDName  = 'refreshProcess'

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
		refresh = vars.get('refresh')
		
		if session_id == "" or session_type == "" or browser_id == ""\
				or user_id == "" or bcc_id == "" or refresh == "":
					self._protocol.quickResponse(MISSING_VARS)
					self.SetDone()
					defer.returnValue(None)	


		refresh_requests = refresh.split()
		sessionCache = SessionsRedis()
		cookies = sessionsCookies()
		res= yield sessionCache.getSessionInfo(session_id,session_type,bcc_id,user_id)
		if not res:
			#If the session loading returns false, then that means it got expired....
			cookies.cookieSessionInfo["browser_id"] = browser_id
			response = yield DummySession(cookies,browser_info,bcc_id,new_browser_id=False)
			self._writeBack(response)
			self.SetDone()
			defer.returnValue(None)		
		
		update_MSESID = False
		update_BSESINFO = False
		for req in refresh_requests:
			if req == "hijack_token-refresh":
				#check if the is no othe rrequest just updated the hijack-token, isnure that within the last 30 seconds no one touched the session
				if now_time() - sessionCache.SessionInfo["hijack_token_update_time"] > HiJack_refresh_rate \
						and now_time() - sessionCache.SessionInfo["last_request_time"] >30:
							sessionCache.SessionInfo["hijack_token"] = random_string_generator(6)
							sessionCache.SessionInfo["hijack_token_update_time"] = now_time()
							yield sessionCache.autoSave()
							update_MSESID = True
			elif req == "hijack_token-synch":
				#Just read from the cache into the cookies
				update_MSESID = True
							
					
		
		
		if sessionCache.SessionInfo["is_permenant"] == "1":
			life_sapn = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["Permenant_life_sapn"]
			context_time = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["Permenant_context_time"]
		else:
			life_sapn = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["life_sapn"] 	
			context_time = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["context_time"]

		
		cookies.load_browserid_fromRedis(sessionCache)
		cookies.load_BSESINFO_fromRedis(sessionCache)
		cookies.load_MSESID_fromRedis(sessionCache)
		cookies.build_MSESID_cookie()
		cookies.build_BSESINFO_cookie()
		cookies.build_browserid_cookie()		
 
		response = SessionResponse.responseFromSessionCache( \
				2,"","0", \
				sessionCache,context_time,life_sapn, \
				update_MSESID,cookies.MSESID_generated_cookie,sessionCache.SessionInfo["is_permenant"], \
				update_BSESINFO,cookies.BSESINFO_generated_cookie, \
				False,cookies.browser_id_generated_cookie)	
		
		#FORCE allow_multi_bcc
		#redis_instance2
		self._writeBack(response)
		
		self.SetDone()
		defer.returnValue(None)	
		
		
		
		
		