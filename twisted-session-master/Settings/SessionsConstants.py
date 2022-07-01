SESSIONS_CONSTANTS = {}



DUMMY_SESSION = {}
DUMMY_SESSION["session_type"] = "0"
DUMMY_SESSION["life_sapn"] = "28800"
DUMMY_SESSION["context_time"] = "14400"
DUMMY_SESSION["Permenant_life_sapn"] = "0"
DUMMY_SESSION["Permenant_context_time"] = "0"
SESSIONS_CONSTANTS[DUMMY_SESSION["session_type"]] = DUMMY_SESSION


MOBILE_APP_SESSION = {}
MOBILE_APP_SESSION["session_type"] = "1"
MOBILE_APP_SESSION["life_sapn"] = "172800"
MOBILE_APP_SESSION["context_time"] = "28800"
MOBILE_APP_SESSION["Permenant_life_sapn"] = "7776000"
MOBILE_APP_SESSION["Permenant_context_time"] = "86400"
SESSIONS_CONSTANTS[MOBILE_APP_SESSION["session_type"]] = MOBILE_APP_SESSION

BROWSER_SESSION = {}
BROWSER_SESSION["session_type"] = "2"
BROWSER_SESSION["life_sapn"] = "172800"
BROWSER_SESSION["context_time"] = "28800"
BROWSER_SESSION["Permenant_life_sapn"] = "7776000"
BROWSER_SESSION["Permenant_context_time"] = "86400"
SESSIONS_CONSTANTS[BROWSER_SESSION["session_type"]] = BROWSER_SESSION


MOBILE_BROWSER_SESSION=  {}
MOBILE_BROWSER_SESSION["session_type"] = "3"
MOBILE_BROWSER_SESSION["life_sapn"] = "172800"
MOBILE_BROWSER_SESSION["context_time"] = "28800"
MOBILE_BROWSER_SESSION["Permenant_life_sapn"] = "7776000"
MOBILE_BROWSER_SESSION["Permenant_context_time"] = "86400"
SESSIONS_CONSTANTS[MOBILE_BROWSER_SESSION["session_type"]] = MOBILE_BROWSER_SESSION


SMS_BECOME_USER_SESSION = {}
SMS_BECOME_USER_SESSION["session_type"] = "4"
SMS_BECOME_USER_SESSION["life_sapn"] = "3600"
SMS_BECOME_USER_SESSION["context_time"] = "3600"
SMS_BECOME_USER_SESSION["Permenant_life_sapn"] = "0"
SMS_BECOME_USER_SESSION["Permenant_context_time"] = "0"
SESSIONS_CONSTANTS[SMS_BECOME_USER_SESSION["session_type"]] = SMS_BECOME_USER_SESSION


SMS_SESSION = {}
SMS_SESSION["session_type"] = "5"
SMS_SESSION["life_sapn"] = "46800"
SMS_SESSION["context_time"] = "43200"
SMS_SESSION["Permenant_life_sapn"] = "0"
SMS_SESSION["Permenant_context_time"] = "0"
SESSIONS_CONSTANTS[SMS_SESSION["session_type"]] = SMS_SESSION


CRM_SESSION = {}
CRM_SESSION["session_type"] = "6"
CRM_SESSION["life_sapn"] = "43200"
CRM_SESSION["context_time"] = "28800"
CRM_SESSION["Permenant_life_sapn"] = "0"
CRM_SESSION["Permenant_context_time"] = "0"
SESSIONS_CONSTANTS[CRM_SESSION["session_type"]] = CRM_SESSION




HiJack_refresh_rate = 1800
last_request_refresh_rate = 900



__all__ = ["DUMMY_SESSION","HiJack_refresh_rate","SESSIONS_CONSTANTS","SMS_BECOME_USER_SESSION","MOBILE_APP_SESSION","last_request_refresh_rate"]
