from Sessions import *
import random
from utils.commandsClient.baytCommand import bayt_command
from twisted.internet import defer
from log.log import *
from Settings.SessionsConstants import *
from ResponseFormatter import SessionResponse
from utils.commandsClient.ERRORS import *
class SessionsCount(bayt_command):
	CMDName  = 'SessionsCount'

	@defer.inlineCallbacks
	def postWrite(self):


		info= yield SessionsRedis.get_sessions_counts()

		self._writeBack( info)
		self.SetDone()
		defer.returnValue(None)	
		
		
		
		
		