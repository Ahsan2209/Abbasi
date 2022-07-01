class SessionResponse:
	@staticmethod
	def responseFromSessionCache(
		status,refresh,brand_new,
		sessionCache,context_time,lifespan,
		modify_MSESID,MSESID_generated_cookie,MSESID_persistent,
		modify_BSESINFO,BSESINFO_generated_cookie,
		modify_browser_id,browser_id_generated_cookie,userKickedOut=0, debug=False):
		if refresh == []:
			refresh = ""
		response = {}
		response["STATUS"] = status
		response["REFRESH"] = refresh
		response["userKickedOut"] = userKickedOut
		response["SECURE"] = "0" if sessionCache.SessionInfo["secure_token"] == "" else "1"
		response["COOKIES"]  = []		
		MSESID_cookie = {}
		MSESID_cookie["COOKIE_NAME"] = "MSESID"
		MSESID_cookie["COOKIE_VALUE"] = MSESID_generated_cookie
		response["COOKIES"].append(MSESID_cookie)
		BSESINFO_cookie = {}
		BSESINFO_cookie["COOKIE_NAME"] = "BSESINFO"
		BSESINFO_cookie["COOKIE_VALUE"] = BSESINFO_generated_cookie
		response["COOKIES"].append(BSESINFO_cookie)
		browserid_cookie = {}
		browserid_cookie["COOKIE_NAME"] = "browser_id"
		browserid_cookie["COOKIE_VALUE"] = browser_id_generated_cookie
		response["COOKIES"].append(browserid_cookie)
		response["COOKIES_OPERATIONS"] = []
		MSESID_cookie_operation = {}
		
		if modify_MSESID:
			if MSESID_generated_cookie is not None and MSESID_generated_cookie != "":
				MSESID_cookie_operation["OPERATION"] = "SET"
			else :
				MSESID_cookie_operation["OPERATION"] = "DELETE"
			MSESID_cookie_operation["COOKIE_NAME"] = "MSESID"
			MSESID_cookie_operation["IS_PERSISTENT"] = MSESID_persistent
			if MSESID_persistent != "1":
				MSESID_cookie_operation["EXPIRY"] = lifespan
			else:
				MSESID_cookie_operation["EXPIRY"] = ""
			response["COOKIES_OPERATIONS"].append(MSESID_cookie_operation)
			
			
			
		if modify_BSESINFO:
			BSESINFO_cookie_operation = {}
			if BSESINFO_generated_cookie  is not None and BSESINFO_generated_cookie != "":
				BSESINFO_cookie_operation["OPERATION"] = "SET"
			else:
				BSESINFO_cookie_operation["OPERATION"] = "DELETE"
			BSESINFO_cookie_operation["COOKIE_NAME"] = "BSESINFO"
			BSESINFO_cookie_operation["IS_PERSISTENT"] = "0"
			BSESINFO_cookie_operation["EXPIRY"] = lifespan
			response["COOKIES_OPERATIONS"].append(BSESINFO_cookie_operation)
		
		if modify_browser_id:
			browser_id_cookie_operation = {}
			if browser_id_generated_cookie is not None and browser_id_generated_cookie != "":
				browser_id_cookie_operation["OPERATION"] = "SET"
			else:
				browser_id_cookie_operation["OPERATION"] = "DELETE"			
			browser_id_cookie_operation["COOKIE_NAME"] = "browser_id"
			browser_id_cookie_operation["IS_PERSISTENT"] = "1"
			browser_id_cookie_operation["EXPIRY"] = ""
			response["COOKIES_OPERATIONS"].append(browser_id_cookie_operation)
		if response["COOKIES_OPERATIONS"] == []:
			response["COOKIES_OPERATIONS"] = ""
		response["INFO"] = {}
		if debug:
			print 'SESSION_CACHE::ResponseFormatter::responseFromSessionCache::sessionCache.SessionInfo::1::',debug,'::',sessionCache.SessionInfo
		response["INFO"]["SESSION_ID"] = sessionCache.SessionInfo["session_id"] 
		response["INFO"]["BRAND_NEW"] = brand_new		
		response["INFO"]["USER_ID"] = sessionCache.SessionInfo["user_id"]
		response["INFO"]["XSRF_TOKEN"] = sessionCache.SessionInfo["xsrf_token"]
		response["INFO"]["BROWSER_ID"] = sessionCache.SessionInfo["browser_id"]
		response["INFO"]["SESSION_TYPE"] =  sessionCache.SessionInfo["session_type"]
		response["INFO"]["SESSION_EXPIRY"] = lifespan
		response["INFO"]["BCC_ID"] =  sessionCache.SessionInfo["bcc_id"]
		response["INFO"]["MULTI_BCC_SESSIONS"] =  sessionCache.SessionInfo["allow_multi_bcc"]
		response["INFO"]["IS_PERSISTENT"] =  sessionCache.SessionInfo["is_permenant"]
		response["INFO"]["SECURE_TOKEN"] =  sessionCache.SessionInfo["secure_token"]
		response["INFO"]["LOGIN_TIME"] =  sessionCache.SessionInfo["login_time"]
		response["INFO"]["LAST_REQUEST_TIME"] = sessionCache.SessionInfo["last_request_time"]
		response["INFO"]["HIJACK_TOKEN"] = sessionCache.SessionInfo["hijack_token"]
		response["INFO"]["BROWSER_TOKEN"] = sessionCache.SessionInfo["browser_token"]
		response["INFO"]["AUTHENTICATE_TIME"] = sessionCache.SessionInfo["authenticate_time"]
		response["INFO"]["HIJACK_UPDATE_TIME"] = sessionCache.SessionInfo["hijack_token_update_time"]
		response["INFO"]["SESSION_CONTEXT_TIME"] = context_time
		if debug:
			print 'SESSION_CACHE::ResponseFormatter::responseFromSessionCache::sessionCache.SessionInfo::2::',debug,'::',sessionCache.SessionInfo
		
		return response
		
	
	