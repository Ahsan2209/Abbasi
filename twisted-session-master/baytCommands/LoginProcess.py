from Sessions import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
from localCache import bccIDsCache
class LoginProcess(bayt_command):
	CMDName  = 'LoginProcess'

	@defer.inlineCallbacks
	def postWrite(self):
		#Allow python genrator to work, even if there is no internal deferred got fired. 
		def empty():
			pass
		yield defer.maybeDeferred(empty)
		#objects to be used
		vars = self._getVarsList()
		session_id = vars.get('session_id')	
		is_persistent = vars.get('is_persistent')
		allow_bcc_sessions = vars.get('allow_bcc_sessions')
		session_type = vars.get('session_type')
		user_id = vars.get('user_id')
		bcc_id = vars.get('bcc_id')
		browser_id = vars.get('browser_id')
		browser_info = vars.get('browser_info')		
		is_network_bcc = vars.get('is_network_bcc')	
		debug = vars.get('debug')
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::START::',debug
			print 'SESSION_CACHE::LoginProcess::postWrite::VARS::',debug,'::',vars
		if session_id == "" or is_persistent == ""  or \
				allow_bcc_sessions == "" or session_type == "" or user_id == "" or is_network_bcc == "":
					self._protocol.quickResponse(MISSING_VARS)
					self.SetDone()
					defer.returnValue(None)	
		
		if is_network_bcc == "1":
			#If this bcc is a network save the bcc_id for deletion
			yield bccIDsCache.add_new_bcc(bcc_id)
		else :
			yield bccIDsCache.remove_bcc(bcc_id)
		
		
		#Load all cookies:
		sessionCache = SessionsRedis()
		cookies = sessionsCookies(debug)
		res= yield sessionCache.getSessionInfo(session_id,DUMMY_SESSION["session_type"],bcc_id,"0",debug)
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::res::',debug,'::',res
		if not res:
			if debug:
				print 'SESSION_CACHE::LoginProcess::postWrite::NOT RES::',debug
			#If the session loading returns false, then that means it got expired....
			cookies.cookieSessionInfo["browser_id"] = browser_id
			response = yield DummySession(cookies,browser_info,bcc_id,new_browser_id=False)
			self._writeBack(response)
			self.SetDone()
			defer.returnValue(None)		
		
		
		
		sessionCache.SessionInfo["user_id"] = user_id
		sessionCache.SessionInfo["session_type"] = session_type
		sessionCache.SessionInfo["xsrf_token"] =  random_string_generator(6)
		sessionCache.SessionInfo["hijack_token"] = random_string_generator(6)
		sessionCache.SessionInfo["is_permenant"] =  is_persistent
		sessionCache.SessionInfo["secure_token"] =  random_string_generator(6)
		sessionCache.SessionInfo["login_time"] = now_time()
		sessionCache.SessionInfo["authenticate_time"] = str(now_time())
		sessionCache.SessionInfo["allow_multi_bcc"] = allow_bcc_sessions
		sessionCache.SessionInfo["MSESID_to_BSESINFO"] = str(random.randrange(0,99))
		sessionCache.SessionInfo["hijack_token_update_time"] = now_time()
		sessionCache.SessionInfo["xsrf_create_time"] = now_time()
		
		if debug:
			yield sessionCache.autoSave(False, debug)
		else:
			yield sessionCache.autoSave()
		if sessionCache.SessionInfo["is_permenant"] == "1":
			life_sapn = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["Permenant_life_sapn"]
			context_time = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["Permenant_context_time"]
		else:
			life_sapn = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["life_sapn"] 	
			context_time = SESSIONS_CONSTANTS[sessionCache.SessionInfo["session_type"]]["context_time"]		
		
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::BEFORE_load_browserid_fromRedis::',debug,'::',sessionCache.SessionInfo
		cookies.load_browserid_fromRedis(sessionCache)
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::BEFORE_load_BSESINFO_fromRedis::',debug,'::',sessionCache.SessionInfo
		cookies.load_BSESINFO_fromRedis(sessionCache)
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::BEFORE_load_MSESID_fromRedis::',debug,'::',sessionCache.SessionInfo
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.cookieSessionInfo::BEFORE_load_MSESID_fromRedis::',debug,'::',cookies.cookieSessionInfo
		cookies.load_MSESID_fromRedis(sessionCache)
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::AFTER_ALL_LOAD::BEFORE_ANY_BUILD::',debug,'::',sessionCache.SessionInfo
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.cookieSessionInfo::AFTER_ALL_LOAD::BEFORE_ANY_BUILD::',debug,'::',cookies.cookieSessionInfo
		cookies.build_MSESID_cookie()
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::AFTER_build_MSESID_cookie::',debug,'::',sessionCache.SessionInfo
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.MSESID_generated_cookie::AFTER_build_MSESID_cookie::',debug,'::',cookies.MSESID_generated_cookie
		cookies.build_BSESINFO_cookie()
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::AFTER_build_BSESINFO_cookie::',debug,'::',sessionCache.SessionInfo
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.BSESINFO_generated_cookie::AFTER_build_BSESINFO_cookie::',debug,'::',cookies.BSESINFO_generated_cookie
		cookies.build_browserid_cookie()		
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::sessionCache.SessionInfo::AFTER_build_browserid_cookie::',debug,'::',sessionCache.SessionInfo
 
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.MSESID_generated_cookie::BEFORE_responseFromSessionCache::',debug,'::',cookies.MSESID_generated_cookie
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.BSESINFO_generated_cookie::BEFORE_responseFromSessionCache::',debug,'::',cookies.BSESINFO_generated_cookie
			print 'SESSION_CACHE::LoginProcess::postWrite::cookies.browser_id_generated_cookie::BEFORE_responseFromSessionCache::',debug,'::',cookies.browser_id_generated_cookie
		
		response = SessionResponse.responseFromSessionCache( \
				2,"","0", \
				sessionCache,context_time,life_sapn, \
				True,cookies.MSESID_generated_cookie,sessionCache.SessionInfo["is_permenant"], \
				True,cookies.BSESINFO_generated_cookie, \
				False,cookies.browser_id_generated_cookie, 0, debug)	
		
		#FORCE allow_multi_bcc
		#redis_instance2
		if debug:
			print 'SESSION_CACHE::LoginProcess::postWrite::response::',debug,'::',response
			
		self._writeBack(response)
				
		if allow_bcc_sessions != "1":
			yield sessionCache.deleteOtherBccsSessions()
			
		self.SetDone()
		defer.returnValue(None)	
			
			
			
			
			