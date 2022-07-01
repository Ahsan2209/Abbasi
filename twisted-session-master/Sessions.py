import urllib
from utils.RedisInterface import sessionsViewCache,sessionsViewReadCache,userViewCache
import time
import random
import string
import binascii
import hashlib
from twisted.internet import defer
import ast
from Settings.SessionsConstants import *
from localCache import bccIDsCache
def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.sample(chars,size))
def now_time():
	return int(time.time() - 1324512000)


class sessionsCookies:
	
	md5_list = {}
	md5_list[0] = "Th1kr@ll@h shre@h"
	md5_list[1] = "Sphinx is cool"
	md5_list[2] = "AOL socks"
	md5_list[3] = "Python rocks"
	md5_list[4] = "I hate PHP"
	md5_list[5] = "Nothing beats C never"
	md5_list[6] = "TCL is oudated language"
	md5_list[7] = "Oracle is ok, but isa costly soloution"
	md5_list[8] = "Postgres is a nice one, mysql now is oracle's'"
	md5_list[9] = "Good bye, md5 list is done"
	debug = False
	
	def __init__(self, debug=False):
		self.cookieSessionInfo = {}
		self.cookieSessionInfo["session_id"] = ""
		self.cookieSessionInfo["user_id"] = ""
		self.cookieSessionInfo["session_type"] = ""
		self.cookieSessionInfo["bcc_id"] = ""
		self.cookieSessionInfo["hijack_token"] = ""
		self.cookieSessionInfo["is_permenant"] = ""
			
		
		self.cookieSessionInfo["MSESID_to_BSESINFO"] = ""
		self.cookieSessionInfo["xsrf_token"] = ""
		self.cookieSessionInfo["authenticate_time"] = ""
		self.cookieSessionInfo["secure_token"] = ""		
		
		self.cookieSessionInfo["browser_id"] = ""
		
		self.MSESID_generated_cookie = ""
		self.BSESINFO_generated_cookie = ""
		self.browser_id_generated_cookie = ""
		self.debug = debug
		if debug:
			print 'SESSION_CACHE::SESSIONS::sessionsCookies::INIT::',self.debug
		#INFO SAVED IN CACHE BUT NOT IN --MSESID-- Cookie.
		#hijack_token_update_time
		#Last hijack_token_update
		#is_permenant_session
		#login_time
		#allow_multibleSessions
		#browser_info_key
		#last_request_time
		
		
		
	def parse_MSESID_cookie(self,MSESID_cookie):
		#returns : 0 -- Hijacked
		#returns : 1 -- New Session
		#returns :2 -- continue
		
		
		#Get the cookie information
		#cookie Format:
		#Session ID
		#User-ID
		#Session Type
		#bcc_id
		#hijack_token
		#SALT_KEY_INDEX
		#MD5 --
		
		if MSESID_cookie is None or MSESID_cookie == "":
			return 1
		MSESID_cookie = urllib.unquote_plus(MSESID_cookie)
		MSESID = MSESID_cookie.split(',')
		if len(MSESID) != 8:
			return 0
		session_id = MSESID[0]
		user_id = MSESID[1]
		session_type = MSESID[2]
		bcc_id = MSESID[3]
		hijack_token = MSESID[4]
		is_permenant = MSESID[5]
		md5_string = session_id + user_id + session_type + bcc_id + hijack_token + is_permenant
		salt_key_index = MSESID[6]
		if not salt_key_index.isdigit():
			return 0
		md5_string +=self.md5_list[int(salt_key_index)]
		hashlib.md5(md5_string).hexdigest()
		if MSESID[7] != hashlib.md5(md5_string).hexdigest():
			return 0
		self.cookieSessionInfo["session_id"] = session_id
		self.cookieSessionInfo["user_id"] = user_id
		self.cookieSessionInfo["session_type"] = session_type
		self.cookieSessionInfo["bcc_id"] = bcc_id
		self.cookieSessionInfo["hijack_token"] = hijack_token
		self.cookieSessionInfo["is_permenant"] = is_permenant
		return 2		
		
		
		
		
	def parse_BSESINFO_cookie(self,BSESINFO_cookie):
		#Get The cookie Information:
		#MSESID_to_BSESINFO
		#xsrf_token
		#authenticate time
		#secure_token
		#returns : 0 -- Hijacked
		#returns : 1 -- EMPTY
		#returns :2 -- continue
		if BSESINFO_cookie is None or BSESINFO_cookie == "":
			return 1
		BSESINFO_cookie = urllib.unquote_plus(BSESINFO_cookie)
		BSESINFO = BSESINFO_cookie.split(',')
		if len(BSESINFO) != 4:
			return 0		
		self.cookieSessionInfo["MSESID_to_BSESINFO"] = BSESINFO[0]
		self.cookieSessionInfo["xsrf_token"] = BSESINFO[1]
		self.cookieSessionInfo["authenticate_time"] = BSESINFO[2]
		self.cookieSessionInfo["secure_token"] = BSESINFO[3]	
		return 2
		
	def parse_browserid_cookie(self,browserid_cookie):
		#returns : True -- EMPTY
		#returns :False -- continue		
		#browser_id
		if browserid_cookie is None or browserid_cookie == "":
			return True	
		browserid_cookie = urllib.unquote_plus(browserid_cookie)
		self.cookieSessionInfo["browser_id"] = browserid_cookie
		return False
	
	def build_MSESID_cookie(self):
		if self.debug:
			print 'SESSION_CACHE::SESSIONS::build_MSESID_cookie::self.cookieSessionInfo::1::',self.debug,'::',self.cookieSessionInfo
		MSESID = []
		salt_key_index	= random.randrange(0, 10)
		MSESID.append(self.cookieSessionInfo["session_id"])
		MSESID.append(self.cookieSessionInfo["user_id"])
		MSESID.append (self.cookieSessionInfo["session_type"])
		MSESID.append(self.cookieSessionInfo["bcc_id"])
		MSESID.append(self.cookieSessionInfo["hijack_token"])
		MSESID.append(self.cookieSessionInfo["is_permenant"])
		MSESID.append(str(salt_key_index))
		if self.debug:
			print 'SESSION_CACHE::SESSIONS::build_MSESID_cookie::self.cookieSessionInfo::2::',self.debug,'::',self.cookieSessionInfo
			print 'SESSION_CACHE::SESSIONS::build_MSESID_cookie::MSESID::AFTER_APPEND::',self.debug,'::',MSESID
		md5_string = MSESID[0] + MSESID[1] + MSESID[2] + MSESID[3] + MSESID[4] +MSESID[5]+ self.md5_list[salt_key_index]
		MSESID.append(hashlib.md5(md5_string).hexdigest())
				
		if self.debug:
			print 'SESSION_CACHE::SESSIONS::build_MSESID_cookie::self.cookieSessionInfo::3::',self.debug,'::',self.cookieSessionInfo
		if self.debug:
			print 'SESSION_CACHE::SESSIONS::build_MSESID_cookie::MSESID::AFTER_APPEND_md5_string::',self.debug,'::',MSESID
		MSESID_cookie = ','.join(MSESID)
		if self.debug:
			print 'SESSION_CACHE::SESSIONS::build_MSESID_cookie::MSESID_cookie::AFTER_JOIN::',self.debug,'::',MSESID_cookie
		
		self.MSESID_generated_cookie = urllib.quote_plus(MSESID_cookie)
		
		
		
	def build_BSESINFO_cookie(self):
		BSESINFO = []
		BSESINFO.append(self.cookieSessionInfo["MSESID_to_BSESINFO"])
		BSESINFO.append(self.cookieSessionInfo["xsrf_token"])
		BSESINFO.append(self.cookieSessionInfo["authenticate_time"])
		BSESINFO.append(self.cookieSessionInfo["secure_token"])
		BSESINFO_cookie = ','.join(BSESINFO)
		if self.debug:
			print 'SESSION_CACHE::SESSIONS::build_BSESINFO_cookie::self.cookieSessionInfo::',self.debug,'::',self.cookieSessionInfo
			print 'SESSION_CACHE::SESSIONS::build_BSESINFO_cookie::BSESINFO_cookie::AFTER_JOIN::',self.debug,'::',BSESINFO_cookie
		self.BSESINFO_generated_cookie = urllib.quote_plus(BSESINFO_cookie) 

		
	def build_browserid_cookie(self):
		self.browser_id_generated_cookie = urllib.quote_plus(self.cookieSessionInfo["browser_id"])		

		
	def load_browserid_fromRedis(self,sessionCache):
		self.cookieSessionInfo["browser_id"] = sessionCache.SessionInfo["browser_id"]
		
	def load_BSESINFO_fromRedis(self,sessionCache):
		self.cookieSessionInfo["MSESID_to_BSESINFO"] = sessionCache.SessionInfo["MSESID_to_BSESINFO"]
		self.cookieSessionInfo["xsrf_token"] = sessionCache.SessionInfo["xsrf_token"]
		self.cookieSessionInfo["authenticate_time"] = sessionCache.SessionInfo["authenticate_time"]
		self.cookieSessionInfo["secure_token"] = sessionCache.SessionInfo["secure_token"]
	
	def load_MSESID_fromRedis(self,sessionCache):
		self.cookieSessionInfo["session_id"] = sessionCache.SessionInfo["session_id"]
		self.cookieSessionInfo["user_id"] = sessionCache.SessionInfo["user_id"]
		self.cookieSessionInfo["session_type"] = sessionCache.SessionInfo["session_type"]
		self.cookieSessionInfo["bcc_id"] = sessionCache.SessionInfo["bcc_id"]
		self.cookieSessionInfo["hijack_token"] = sessionCache.SessionInfo["hijack_token"]		
		self.cookieSessionInfo["is_permenant"] = sessionCache.SessionInfo["is_permenant"]	
	
	
	
	
class SessionsRedis:
	SessionInfo = {}
	def __init__(self):
		self.SessionInfo["session_id"] = ""
		self.SessionInfo["user_id"] = ""
		self.SessionInfo["session_type"] = ""
		self.SessionInfo["browser_id"] = ""	
		self.SessionInfo["xsrf_token"] = ""
		self.SessionInfo["hijack_token"] = ""
		self.SessionInfo["is_permenant"] = ""
		self.SessionInfo["secure_token"] = ""
		self.SessionInfo["login_time"] = ""
		self.SessionInfo["authenticate_time"] = ""
		self.SessionInfo["last_request_time"] = ""
		self.SessionInfo["allow_multi_bcc"] = ""
		self.SessionInfo["browser_token"] = ""
		self.SessionInfo["MSESID_to_BSESINFO"] = ""
		self.SessionInfo["hijack_token_update_time"] = ""
		self.SessionInfo["bcc_id"] = ""
		self.SessionInfo["xsrf_create_time"] = ""
	
	@staticmethod
	def createBrowserToken(browser_info):
		token =  binascii.crc32(browser_info) & 0xffffffff
		return token
	
	def CreateDummySession(self,session_id,browser_id,bcc_id,browser_info,redis_instance, debug=False):
		cleanRedis = False
		self.SessionInfo["session_id"] = session_id
		self.SessionInfo["user_id"] = "0"
		self.SessionInfo["session_type"] = DUMMY_SESSION["session_type"]
		self.SessionInfo["browser_id"] = browser_id	
		self.SessionInfo["xsrf_token"] = random_string_generator(6)
		self.SessionInfo["hijack_token"] = random_string_generator(6)
		self.SessionInfo["is_permenant"] = "0"
		self.SessionInfo["secure_token"] = ""
		self.SessionInfo["login_time"] = ""
		self.SessionInfo["authenticate_time"] = ""
		self.SessionInfo["last_request_time"] = now_time()
		self.SessionInfo["allow_multi_bcc"] = "0"
		self.SessionInfo["browser_token"] = SessionsRedis.createBrowserToken(browser_info)
		self.SessionInfo["MSESID_to_BSESINFO"] = str(random.randrange(0,99))
		self.SessionInfo["bcc_id"] = bcc_id
		self.SessionInfo["hijack_token_update_time"] = now_time()
		self.SessionInfo["xsrf_create_time"] = now_time()
		
		
		def cleanMyRedis():
			redis_instance.CloseConnection()
		
		if redis_instance is None:
			cleanRedis = True
			redis_instance  = sessionsViewCache()	
					
		if debug:
			print 'SESSION_CACHE::SESSIONS::CREATE_DUMMY_SESSION::BEFORE_SETEX::STR::',debug,'::',self.SessionInfo
		d = redis_instance.Redisfull_send("SETEX","SESSION_%s" % session_id, DUMMY_SESSION["life_sapn"], str(self.SessionInfo))
		
		if cleanRedis:
			d.addCallback(cleanMyRedis)
		return d
	
	
	@staticmethod
	def get_simpleSessionInfo(session_id):
		redis_instance1  = sessionsViewReadCache()
		d =  redis_instance1.Redisfull_send("GET","SESSION_%s" % session_id)
		def reply(*args):
			redis_instance1.CloseConnection()
			session_by_id  =  args[0]
			if session_by_id is None:
				return {}
			else:
				Info =  ast.literal_eval(session_by_id)
				return Info
		d.addCallback(reply)
		return d
				
	def getSessionInfo(self,session_id,session_type,bcc_id,user_id,debug=False):
		
		if debug:
			print 'SESSION_CACHE::Sessions::getSessionInfo::START::',debug
		redis_instance1  = sessionsViewCache()
		redis_instance2   = userViewCache()
		redis_instance3  = sessionsViewReadCache()

		
		d1 = redis_instance3.Redisfull_send("GET","SESSION_%s" % session_id)
		if user_id == "0":
			d = d1
		else:
			d2 = redis_instance2.Redisfull_send("GET","USER_SESSION_%s_%s_%s" % (user_id,session_type,bcc_id))
			d= defer.DeferredList([d1,d2])
	
		def loadIfExists(*args):
			if debug:
				print 'SESSION_CACHE::Sessions::loadIfExists::START::',debug
			session_by_user_id = None
			if debug:
				print 'SESSION_CACHE::Sessions::loadIfExists::ARGS::',debug,'::',args
			
			
			if user_id == "0":
				session_by_id  =  args[0]
			else:
				session_by_id = args[0][0][1]
				session_by_user_id = args[0][1][1]
			if session_by_id is None or (user_id != "0" and session_by_user_id is None):
				return False
			#So far so good.
			
			#load all variables from cache:
			self.SessionInfo =  ast.literal_eval(session_by_id)
			if user_id != self.SessionInfo["user_id"]:
				return False
			if user_id != "0":
				#check if the user id is linked to the same session
				sessionInfo_user =  ast.literal_eval(session_by_user_id)
				if sessionInfo_user != self.SessionInfo:
					return False
			if debug:
				print 'SESSION_CACHE::Sessions::loadIfExists::RETURN_TRUE::',debug
			return True
					
		d.addCallback(loadIfExists)
		
		def resetIfNeeded(*args):
			if debug:
				print 'SESSION_CACHE::Sessions::resetIfNeeded::START::',debug
			if args[0]:
				return "AA"
			if debug:
				print 'SESSION_CACHE::Sessions::resetIfNeeded::NOT_DELETE_SESSION_FROM_CACHE::',debug
				return True
			#Delete the session value from cache.
			return redis_instance1.Redisfull_send("DEL","SESSION_%s" % session_id)
			#return True
		d.addCallback(resetIfNeeded)
		
		def cleanMysessionsViewCache(*args):
			if debug:
				print 'SESSION_CACHE::Sessions::cleanMysessionsViewCache::START::',debug
				print 'SESSION_CACHE::Sessions::cleanMysessionsViewCache::ARGS::',debug,'::',args
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()
			redis_instance3.CloseConnection()
			if args[0] == "AA":
				return True
			if debug:
				print 'SESSION_CACHE::Sessions::cleanMysessionsViewCache::RETURN_FALSE::',debug
			return False 
				
		d.addCallback(cleanMysessionsViewCache)
		

		return d
		
	def refresh_session_timeout(self):
		self.SessionInfo["last_request_time"] = now_time()
		redis_instance1  = sessionsViewCache()
		redis_instance2   = userViewCache()			
		if self.SessionInfo["is_permenant"] == "1":
			ttl = SESSIONS_CONSTANTS[self.SessionInfo["session_type"]]["Permenant_life_sapn"]
		else:
			ttl = SESSIONS_CONSTANTS[self.SessionInfo["session_type"]]["life_sapn"] 
		d1 = redis_instance1.Redisfull_send("EXPIRE","SESSION_%s" % self.SessionInfo["session_id"],ttl)
		if self.SessionInfo["user_id"] == "0":
			d = d1
		else:
			d2 = redis_instance2.Redisfull_send("EXPIRE","USER_SESSION_%s_%s_%s" % (self.SessionInfo["user_id"],self.SessionInfo["session_type"],self.SessionInfo["bcc_id"]),ttl)
			d= defer.DeferredList([d1,d2])
		def cleanMysessionsViewCache(*args):
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()
		d.addCallback(cleanMysessionsViewCache)
		return d		
		
	def autoSave(self,update_BSESINFO = False, debug=False):
		
		self.SessionInfo["last_request_time"] = now_time()
		if update_BSESINFO:
			self.SessionInfo["xsrf_create_time"] = now_time()
		redis_instance1  = sessionsViewCache()
		redis_instance2   = userViewCache()			
		if self.SessionInfo["is_permenant"] == "1":
			ttl = SESSIONS_CONSTANTS[self.SessionInfo["session_type"]]["Permenant_life_sapn"]
		else:
			ttl = SESSIONS_CONSTANTS[self.SessionInfo["session_type"]]["life_sapn"] 
		
		if debug:
			print 'SESSION_CACHE::Sessions::AUTO_SAVE::1::BEFORE_SETEX::STR::',debug,'::',self.SessionInfo
		d1 = redis_instance1.Redisfull_send("SETEX","SESSION_%s" % self.SessionInfo["session_id"],ttl,str(self.SessionInfo))
		
		if self.SessionInfo["user_id"] == "0":
			d = d1
		else:
			if debug:
				print 'SESSION_CACHE::Sessions::AUTO_SAVE::2::BEFORE_SETEX::STR::',debug,'::',self.SessionInfo
			d2 = redis_instance2.Redisfull_send("SETEX","USER_SESSION_%s_%s_%s" % (self.SessionInfo["user_id"],self.SessionInfo["session_type"],self.SessionInfo["bcc_id"]),ttl,str(self.SessionInfo))
			d= defer.DeferredList([d1,d2])
		def cleanMysessionsViewCache(*args):
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()
		d.addCallback(cleanMysessionsViewCache)
		return d
	def delete(self):
		redis_instance1  = sessionsViewCache()
		redis_instance2   = userViewCache()			 
		
		d1 = redis_instance1.Redisfull_send("DEL","SESSION_%s" % self.SessionInfo["session_id"])
		if self.SessionInfo["user_id"] == "0":
			d = d1
		else:
			d2 = redis_instance2.Redisfull_send("DEL","USER_SESSION_%s_%s_%s" % (self.SessionInfo["user_id"],self.SessionInfo["session_type"],self.SessionInfo["bcc_id"]))
			d= defer.DeferredList([d1,d2])
		def cleanMysessionsViewCache(*args):
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()
		d.addCallback(cleanMysessionsViewCache)
		return d		
	
	def deleteOtherBccsSessions(self):
		if self.SessionInfo["user_id"] == "0":
			return
		redis_instance2   = userViewCache()	
		redis_instance1   = sessionsViewCache()
		
		d = bccIDsCache.load_from_redis()
		def get_all_sessions(*args):
			keys = []
			for id in bccIDsCache.get_all_bcc_ids():
				if id != self.SessionInfo["bcc_id"]:
					keys.append("USER_SESSION_%s_%s_%s" % (self.SessionInfo["user_id"],self.SessionInfo["session_type"],id))
			if len(keys) == 0:
				keys = ['first_time_login']
			return redis_instance2.Redisfull_send("MGET",*keys)
		d.addCallback(get_all_sessions)
		def prepareToDelete(*args):
			user_delete_list = []
			sessions_delete_list = []
			for val in args[0]:
				if val is not None:
					Info =  ast.literal_eval(val)
					user_delete_list.append("USER_SESSION_%s_%s_%s" % (Info["user_id"],Info["session_type"],Info["bcc_id"]))
					sessions_delete_list.append("SESSION_%s" % Info["session_id"])
			if len(user_delete_list) == 0:
				return True
			d1 = redis_instance1.Redisfull_send("DEL",*sessions_delete_list)
			d2 = redis_instance2.Redisfull_send("DEL",*user_delete_list)
			d= defer.DeferredList([d1,d2])
			return d
		d.addCallback(prepareToDelete)
		
		def cleanMysessionsViewCache(*args):
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()
			return True
		
		d.addCallback(cleanMysessionsViewCache)
		return d
	@staticmethod	
	def deleteUserSessions(user_id):
		redis_instance2   = userViewCache()	
		redis_instance1   = sessionsViewCache()
		d = redis_instance2.Redisfull_send("KEYS","USER_SESSION_%s_*" % user_id)
		def getKeys(*args):
			keys = args[0]
			#exclude my key
			if len(keys) == 0:
				return None
			return redis_instance2.Redisfull_send("MGET",' '.join(keys))
		d.addCallback(getKeys)
		
		def prepareToDelete(*args):
			user_delete_list = []
			sessions_delete_list = []
			if args[0] == [None] or args[0] == None:
				return None
			for key in args[0]:
				Info =  ast.literal_eval(key)
				user_delete_list.append("USER_SESSION_%s_%s_%s" % (user_id,Info["session_type"],Info["bcc_id"]))
				sessions_delete_list.append("SESSION_%s" % Info["session_id"])
				d1 = redis_instance1.Redisfull_send("DEL",' '.join(sessions_delete_list))
				d2 = redis_instance2.Redisfull_send("DEL",' '.join(user_delete_list))
				dx= defer.DeferredList([d1,d2])
				return dx
		d.addCallback(prepareToDelete)
		
		def cleanMysessionsViewCache(*args):
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()
			return True
		
		d.addCallback(cleanMysessionsViewCache)
		return d

	
	@staticmethod	
	def get_sessions_counts():
		redis_instance2   = userViewCache()	
		redis_instance1   = sessionsViewReadCache()
		d1 = redis_instance1.Redisfull_send("DBSIZE")
		d2 = redis_instance2.Redisfull_send("DBSIZE")
		d= defer.DeferredList([d1,d2])
		def getCounts(*args):
			sessions_count = args[0][0][1]
			users_count    = args[0][1][1]
			redis_instance1.CloseConnection()
			redis_instance2.CloseConnection()			
			return [sessions_count,users_count]
		d.addCallback(getCounts)
		return d		
class sessionsSequences:
	@staticmethod
	def browserID_generate(redis_instance):
		def formatMe(*args):
			prefix = now_time()
			browser_id =  "%s%s%s" % (prefix,args[0],random.randrange(0, 100))
			return browser_id
		if redis_instance is None:
			redis_instance  = userViewCache()
			
		d = redis_instance.Redisfull_send("INCR","Browser_ID_SEQ")
		d.addCallback(formatMe)
		return d
	@staticmethod
	def sessionID_generate(redis_instance):
		def formatMe(*args):
			prefix = now_time()
			browser_id =  "%s%s%s" % (prefix,args[0],random.randrange(0, 100))
			return browser_id
		if redis_instance is None:
			redis_instance  = userViewCache()
			
		d = redis_instance.Redisfull_send("INCR","SESSION_ID_SEQ")
		d.addCallback(formatMe)
		return d		
		
	
def DummySession(cookies,browser_info,bcc_id,new_browser_id=False, debug=False):
	if debug:
		print 'SESSION_CACHE::Sessions::DummySession::START::',debug
	#brand new user steps:
	#1-Create New Session_id
	#2-Create New Browser_id
	#3-Create Dummy Session and save to redis
	#4- Create all cookies
	#5-Update Cookies
	#return back
	redis_instance1  = sessionsViewCache()
	redis_instance2 = sessionsViewCache()
	sessionCache = SessionsRedis()
	if new_browser_id:
		d1 = sessionsSequences.browserID_generate(redis_instance1)
		d2 = sessionsSequences.sessionID_generate(redis_instance2)
		
		d= defer.DeferredList([d2,d1])
		
	else:
		d=  sessionsSequences.sessionID_generate(redis_instance2)
	
	def manipulateSequences(*args):
		if new_browser_id:
			browser_id = args[0][1][1]
			session_id = args[0][0][1]
		else:
			browser_id = cookies.cookieSessionInfo["browser_id"]
			session_id = args[0]
		
		return sessionCache.CreateDummySession(session_id,browser_id,bcc_id,browser_info,redis_instance1, debug)
	d.addCallback(manipulateSequences)
	
	def cleanRedisConnections(*args):
		redis_instance1.CloseConnection()
		redis_instance2.CloseConnection()
	d.addCallback(cleanRedisConnections)
	def createCookies(*args):
		cookies.load_browserid_fromRedis(sessionCache)
		cookies.load_BSESINFO_fromRedis(sessionCache)
		cookies.load_MSESID_fromRedis(sessionCache)
		cookies.build_MSESID_cookie()
		cookies.build_BSESINFO_cookie()
		cookies.build_browserid_cookie()
	d.addCallback(createCookies)
	
	
	def respond(*args):
		from ResponseFormatter import SessionResponse
		response = SessionResponse.responseFromSessionCache( \
				"2","","1", \
				sessionCache,DUMMY_SESSION["context_time"], DUMMY_SESSION["life_sapn"], \
				True,cookies.MSESID_generated_cookie,"0", \
				True,cookies.BSESINFO_generated_cookie, \
				new_browser_id,cookies.browser_id_generated_cookie)
		return response	
	d.addCallback(respond)
	
	return d	
	
__all__ = ["sessionsCookies","sessionsSequences","SessionsRedis","now_time","random_string_generator","DummySession"]
