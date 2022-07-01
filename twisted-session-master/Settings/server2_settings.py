#This module contains the default values for all settings used by Bayt Manager.

#Bayt Service application Specific
#1- name : for example you can use BaytLogger
#2-Version: for any update, please update the version here
#3-Developer Owner: the owner of the project development.
#4-Developer : the developer who made the latest change

APPLICATION_NAME = 'Sessions-Management'
APPLICATION_VERSION = '1.0'
DEVELOPER_OWNER = 'Thikrallah Shreah'
DEVELOPER = 'Thikrallah Shreah'

#Bayt Service connection Specific:
#1- port number: The port which the service will listen to.
#2- Max concurrent connection: max number of concurrent connection to the service,it should be equals to the max number of virtual AOLs connection to it:), zero means unlimited

PORT_NUMBER = 7732
MAX_CONNECTION = 0

#DEBUGGING:
#1- DEBUG : enable or disable Debugging
#2- DEBUG FILE: the file the debugging messages will be stored, if nothing provided..logging will be on screen.s
USER = 'user'
PASSWORD = 'password'
DEBUG = True
DEBUG_FILE = 'web-service'
#DEBUG_FILE = ''
sessionsViewCache_REDIS_HOST = '10.52.6.229' 
sessionsViewCache_REDIS_PORT_NUMBER = 6380

userViewCache_REDIS_HOST = '10.52.6.229' 
userViewCache_REDIS_PORT_NUMBER = 6381



