import urllib
from twisted.protocols import basic
from utils.commandsClient.ERRORS import *
from utils.commandsClient.commandsManager import *

from log.log import *
import json
from datetime import datetime

class commandsProtocol(basic.LineReceiver):
	_cmd = None
	
	def writeLine(self,msg):
		response = {}
		response['RESPONSE'] = msg
		responseObj = json.dumps(response)
		self.quickResponse(responseObj)
	def quickResponse(self,responseObj):
		self.transport.write(responseObj+"\r\n")
	def lineReceived(self, command):
		self._status = 1
		self._start_time = datetime.now()
		line = ''
		try:
			line = command
			line = line.split("?")
		except:
			self.quickResponse(PARSING_COMMAND_ERROR)
			bayt_log.logError("Parser", "The input command couldn't be parsed'", command)
		if type(line) is list and len(line) == 2:
			commandName = line[0]
			if commandName is None:
				self.quickResponse(NO_COMMAND_FOUND)
				bayt_log.logError("Parser", "Command is None", command)
			else:
				commandVars = line[1].split("&")
				if commandVars is None or len(commandVars) < 2:
					self.quickResponse("NO VARIABLES ATTACHED!!")
					bayt_log.logError("Parser", "There is no command vars", command)
				else:
					#Bind Variables To JOSN
					commandVarsDic = {}
					for item in commandVars:
						item = item.split("=")
						if len(item) > 0:
							if len(item) > 1:
								commandVarsDic.update({item[0] :urllib.unquote_plus(item[1])})
							else:
								commandVarsDic.update({item[0] : ''})
					#SECURITY CHECK
					userName = commandVarsDic.get('bayt_user')
					password = commandVarsDic.get('user_pass')
					if userName != self.factory.get_userName() or password != self.factory.get_password():
						self.quickResponse("Authentication Failed!")
						bayt_log.logError("Parser", "Authentication Failed!", command)
					else:
						try:					
							commandVars = commandVarsDic
							commandObject = serviceCommands.getCommandObjectByName(commandName)
							if commandObject is None:
								#TODO check reload, version, StopService
								self.quickResponse(COMMAND_NOT_FOUND)
								bayt_log.logError("Parser", "Command not Found", command)
							else:
								self._cmd = commandObject
								self._cmd.setCommandsDependency(self,commandVars)
								commandObject.preWrite()
								commandObject.postWrite()
								
								self.factory.increaseLogCount()
						except Exception as err:
							self.quickResponse(PARSING_COMMAND_ERROR)
							bayt_log.logError(commandName,"ERROR IN Command :\n" , str(err))
		else:
			self.quickResponse(PARSING_COMMAND_ERROR)
			bayt_log.logError("Parser", "Parsing command error", command)

		
	   
		#inactive protocol
			
			

			
	def closeConnectionAtExit(self):
		self._closeAtExit = True	   
	def loseConnection(self):
		self.transport.loseConnection()
	def isActive(self):
		return self._status	 
	def connectionMade(self):
		self.MAX_LENGTH = 128000
		if self.factory.increaseCount():
			bayt_log.logMsg('Number of instances has been reached',True)
			self.transport.loseConnection()
		else:
			self.factory._protocols.append(self)
			self._closeAtExit = False 
			self._status = 0
	def connectionLost(self, reason):
		errorMsg =  reason.getErrorMessage()
		if errorMsg != "Connection was closed cleanly." and errorMsg != "Connection to the other side was lost in a non-clean fashion.":
			bayt_log.logMsg('(TWISTED INTERFACE FOR LOG) -- %s' % errorMsg,True)
		self.factory._protocols.remove(self)
		self.factory.decreaseCount() 