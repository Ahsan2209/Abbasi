"""
This Manager Contains All classes.
Every thing starts From here, from configurations, up to the running Process
Bayt Manager contains the following subModules:
1- Settings Reader , The file is located under settings folder, where it reads all projects Settings, and initialize the other classes with it.
"""
from Settings.settings_manager import *
from utils.commandsClient.commandsManager import *
from localCache import bccIDsCache
from log.log import *
class BaytLoader():
	def __init__(self):
		#Initialize logging
		bayt_log.initialaizeFromSettings(settingsm)
		bayt_log.logMsg('Start Sevice: %s revision:%s' % (settingsm.getItem('APPLICATION_NAME'),settingsm.getItem('APPLICATION_VERSION')))
		bayt_log.logMsg('Latest update From: %s\n If you need any help contact %s' % (settingsm.getItem('DEVELOPER'),settingsm.getItem('DEVELOPER_OWNER')))
		#####
		logMsg = 'Commands Modules loaded:\n'
		for cmd in serviceCommands.getCommandNames():
			logMsg += "%s\n" % cmd
		bayt_log.logMsg(logMsg)
		#####
	from Settings.active_servers import *
	if len(active_servers_settings_files) == 1:		
		d = bccIDsCache.load_from_redis()
		d.callback(1)
	def getPort(self):
		return settingsm.getItem('PORT_NUMBER')  

	def getmaxNumberOfConnecion(self):
		return settingsm.getItem('MAX_CONNECTION')
	def get_userName(self):
		return settingsm.getItem('USER')
	def get_password(self):
		return settingsm.getItem('PASSWORD')	
		
	def get_applicationName(self):
		return settingsm.getItem('APPLICATION_NAME')	
