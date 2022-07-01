from sessions_fix import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
from twisted.internet import reactor


class validationProcess(bayt_command):
	CMDName  = 'validationProcess'
	
	
	
	def Response_hackedSession(self):
		response = SessionResponse.responseFromSessionCache( \
				"0","","0", \
				SessionsRedis(),"0","0", \
				True,None,"0", \
				True,None, \
				True,"")
		
		#Response for hacked session
		self._writeBack(response)	

	def respondBack2(self,*args):
		self._writeBack(args[0])
		self.SetDone()
		return True
	
	
	def dummyBuild(self, debug=False):
		tmp=False
		if hasattr(self, 'sessionCache'):
			tmp=self.sessionCache.userKickedOut
		if debug:
			print 'SESSION_CACHE::validationProcess::dummyBuild::START::',debug
		d = DummySession(self.cookies,self.browser_info,self.bcc_id,new_browser_id=self.new_browser_id,userKickedOut=tmp,debug=debug)
		d.addCallback(self.respondBack2)
		reactor.callLater(0, d.callback,"")
		
	def isExpired(self,*args):
		res = args[0]
		if not res:
			self.dummyBuild()
			return True
		return False
	
	
	def notExpired_checkHacking(self,*args):
		calls_stopped = args[0]
		
		if not calls_stopped:	
			#Compare input values with session from cache.
			#browser has changed --> Results hacked session				
			if SessionsRedis.createBrowserToken(self.browser_info) !=  self.sessionCache.SessionInfo["browser_token"] or \
					self.sessionCache.SessionInfo["bcc_id"] != self.bcc_id or \
					self.cookies.cookieSessionInfo["browser_id"] != self.sessionCache.SessionInfo["browser_id"] :
						self.Response_hackedSession()
						self.SetDone()
						return 0
					
			# if  mapping between MSESID and BSESINFO has changed--> hacked session
			#Checking the Hijack token (HiJack_refresh_rate)refresh
	 		if self.BSESINFO_status == 2 and ( \
							self.sessionCache.SessionInfo["MSESID_to_BSESINFO"] != self.cookies.cookieSessionInfo["MSESID_to_BSESINFO"] or \
							self.sessionCache.SessionInfo["xsrf_token"] != self.cookies.cookieSessionInfo["xsrf_token"] or \
							self.sessionCache.SessionInfo["authenticate_time"] != self.cookies.cookieSessionInfo["authenticate_time"] or \
							self.sessionCache.SessionInfo["secure_token"] != self.cookies.cookieSessionInfo["secure_token"]  ):
								self.Response_hackedSession()
								self.SetDone()
								return True
			if self.sessionCache.SessionInfo["hijack_token"] != self.cookies.cookieSessionInfo["hijack_token"]:
				self.Response_hackedSession()
				self.SetDone()
				return 0					
		
			
			###OK,,,No Problem
			if self.new_session_info:
				self.sessionCache.SessionInfo["MSESID_to_BSESINFO"] = str(random.randrange(0,99))
				self.cookies.cookieSessionInfo["MSESID_to_BSESINFO"] = self.sessionCache.SessionInfo["MSESID_to_BSESINFO"]
				
				self.sessionCache.SessionInfo["xsrf_token"] = random_string_generator(6)
				self.cookies.cookieSessionInfo["xsrf_token"] = self.sessionCache.SessionInfo["xsrf_token"]
				self.sessionCache.SessionInfo["authenticate_time"] = ""
				self.cookies.cookieSessionInfo["authenticate_time"] = self.sessionCache.SessionInfo["authenticate_time"]
				self.sessionCache.SessionInfo["secure_token"] = ""
				self.cookies.cookieSessionInfo["secure_token"] = self.sessionCache.SessionInfo["secure_token"]
				self.cookies.load_BSESINFO_fromRedis(self.sessionCache)
				self.cookies.build_BSESINFO_cookie()
				self.BSESINFO_cookie = self.cookies.BSESINFO_generated_cookie
				#We need to save the session to cache.
				return 2			
			return 1	
		
		return 0	
	
	def autoSave_andreply(self,*args):
		if args[0] == 2:
			d = self.sessionCache.autoSave(update_BSESINFO=True)
			reactor.callLater(0, d.callback,"");#ASYNCH
		
		if args[0] != 0:
			if self.sessionCache.SessionInfo["is_permenant"] == "1":
				life_sapn = SESSIONS_CONSTANTS[self.sessionCache.SessionInfo["session_type"]]["Permenant_life_sapn"]
				context_time = SESSIONS_CONSTANTS[self.sessionCache.SessionInfo["session_type"]]["Permenant_context_time"]
			else:
				life_sapn = SESSIONS_CONSTANTS[self.sessionCache.SessionInfo["session_type"]]["life_sapn"] 	
				context_time = SESSIONS_CONSTANTS[self.sessionCache.SessionInfo["session_type"]]["context_time"]	
			response = SessionResponse.responseFromSessionCache( \
					str(args[0]),[],"0", \
					self.sessionCache,context_time,life_sapn, \
					False,self.MSESID_cookie,self.sessionCache.SessionInfo["is_permenant"], \
					self.new_session_info,self.BSESINFO_cookie, \
					False,self.browserid_cookie)					
			
			self._writeBack(response)
			self.SetDone()	

	
	def postWrite(self):
		#Allow python genrator to work, even if there is no internal deferred got fired. 
		#objects to be used
		self.cookies = sessionsCookies()
		
		#command variables:
		self.new_browser_id = False
		new_session_id = False
		self.new_session_info = False
		
		
		vars = self._getVarsList()
		self.MSESID_cookie = vars.get('MSESID')
		self.BSESINFO_cookie = vars.get('BSESINFO')
		self.browserid_cookie = vars.get('browser_id')
		self.browser_info = vars.get('browser_info')			
		self.bcc_id = vars.get('bcc_id')
		debug = vars.get('debug')
		if debug:
			print 'SESSION_CACHE::validationProcess::postWrite::START::',debug
		#Load all cookies:
		MSESID_status = self.cookies.parse_MSESID_cookie(self.MSESID_cookie)
		self.BSESINFO_status = self.cookies.parse_BSESINFO_cookie(self.BSESINFO_cookie)
		browser_id_status = self.cookies.parse_browserid_cookie(self.browserid_cookie)
		#CHECK COOKIES HACKING
		#If the MSESID cookie is hacked 
		#OR BSESINFO cookie is hacked
		#Or the MSESID exists or BSESINFO cookie exist and there is no browser id cookie
		#Or BSESINFO cookie exists and MSESID doesn't exist
		#Or BSESINFO doesn't exist and the session is not permenant 
		#--> Results hacked status
		if MSESID_status ==  0 or self.BSESINFO_status == 0 \
				or ((MSESID_status == 2 or self.BSESINFO_status == 2) and browser_id_status) \
				or (MSESID_status == 1 and self.BSESINFO_status ==2) \
				or (self.BSESINFO_status == 1 and self.cookies.cookieSessionInfo["is_permenant"] == "0"  ):
					#Report hacked status
					self.Response_hackedSession()
					self.SetDone()
					return False
		if browser_id_status:
			#Note: New browser ID will create new Session_id and new info
			self.new_browser_id = True 
		elif MSESID_status == 1:
			#Note new session id will create new info
			new_session_id = True
		if self.BSESINFO_status == 1:
			self.new_session_info = True

		if self.new_browser_id or  new_session_id:
			self.dummyBuild(debug)
			return True	
			#DONE.....	

		#There is a Session and browserID --> get the session from cache.
		self.sessionCache = SessionsRedis(debug)
		d = self.sessionCache.getSessionInfo(self.cookies.cookieSessionInfo["session_id"],self.cookies.cookieSessionInfo["session_type"],\
						self.cookies.cookieSessionInfo["bcc_id"],self.cookies.cookieSessionInfo["user_id"])
		d2  = d.addCallback(self.isExpired)	
		d3 = d2.addCallback(self.notExpired_checkHacking)
		d4 = d3.addCallback(self.autoSave_andreply)
		
		reactor.callLater(0, d4.callback,"")
		return False
		