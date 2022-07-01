from utils.commandsClient.baytCommand import bayt_command
from log.log import *
from utils.commandsClient.ERRORS import *
class reload(bayt_command):
	CMDName  = 'reload'
	
	def preWrite(self):
		from utils.commandsClient.commandsManager import serviceCommands
		vars = self._getVarsList()
		file_to_reload =  vars.get('filter')
		if serviceCommands.ReLoadCommandFile(file_to_reload) is True:
			self._quickResponse(NO_ERROR) 
		else:
			self._quickResponse('ERROR') 
		bayt_log.logMsg('Loading '+ file_to_reload)
	
	def postWrite(self):
		self.SetDone()
		pass