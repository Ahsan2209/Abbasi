from twisted.protocols import basic
from utils.commandsClient.ERRORS import *
from utils.commandsClient.commandsManager import *

#from twisted.internet import protocol
#from twisted.internet.defer import Deferred
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
			line = json.loads(command) 
		except:
			self.quickResponse(PARSING_COMMAND_ERROR)
			bayt_log.logError("Parser", "The input command couldn't be parsed'", command)
		if type(line) is list:
			line = line[0]
			commandName = line.get('cmd')
			if commandName is None:
				self.quickResponse(NO_COMMAND_FOUND)
				bayt_log.logError("Parser", "The input command is None", command)
			else:
				commandVars = line.get('vars')
				if commandVars is None:
					self.quickResponse(NO_VARS)
					bayt_log.logError("Parser", "The input command has no vars", command)
				else:
					#SECURITY CHECK
					userName = line.get('bayt_user')
					password = line.get('user_pass')
					if userName != self.factory.get_userName() or password != self.factory.get_password():
						self.quickResponse("Authentication Failed!")
						bayt_log.logError("Parser", "The input command isn't authenticated'", command)
					else:
						try:
							commandVars = json.loads(commandVars)
							commandObject = serviceCommands.getCommandObjectByName(commandName)
							if commandObject is None:
								#TODO check reload, version, StopService
								self.quickResponse(COMMAND_NOT_FOUND)
								bayt_log.logError("Parser", "The input command Not found'", command)
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
			bayt_log.logError("Parser", "The input command is not var", command)

		
	   
		#inactive protocol
			
						

					
	def closeConnectionAtExit(self):
		self._closeAtExit = True	   
	def loseConnection(self):
		self.transport.loseConnection()
	def isActive(self):
		return self._status	 
	def connectionMade(self):
		if self.factory.increaseCount():
			bayt_log.logMsg('Number of instances has been reached')
			self.transport.loseConnection()
		else:
			self.factory._protocols.append(self)
			self._closeAtExit = False 
			self._status = 0
	def connectionLost(self, reason):
		self.factory._protocols.remove(self)
		self.factory.decreaseCount() 