import sys
import __builtin__

file_to_reload = ""
if (len(sys.argv) > 1):
	__builtin__.mySettingFile = "Settings/"  + sys.argv[1] 
	file_to_reload = sys.argv[2]



from subprocess import *
import os
from Settings.settings_manager import *
from twisted.internet import reactor , protocol
from twisted.protocols import basic
import subprocess
from utils.commandsClient.baytCommand import bayt_command
from log.log import *


port  = settingsm.getItem('PORT_NUMBER')
user = settingsm.getItem('USER')
password =  settingsm.getItem('PASSWORD')

class simpleClient(basic.LineReceiver):   
	def connectionMade(self):
		print 'Reloading'
		cmdPacket = '[{"cmd" : "reload","bayt_user" : "'+user+'","user_pass" : "'+password+'","vars" : "[{\\"filter\\" : \\"'+file_to_reload+'\\"}]"}]'
		self.transport.write(cmdPacket+"\r\n")
		
	def dataReceived(self, data):
		self.transport.loseConnection()
	
	def connectionLost(self, reason):
		reactor.stop()

class simpleClientFactory(protocol.ClientFactory):
	protocol = simpleClient	
	servicePID = 0


print 'Send safe shutdown....'
fact = simpleClientFactory()
reactor.connectTCP('localhost', port, fact)
reactor.callLater(5,reactor.stop)
reactor.run()
reactor.callLater(5,reactor.stop)
servicePID = fact.servicePID
print "servicePID : %s" % servicePID
while servicePID != 0 :
	try:
		isDone = os.path.exists("/proc/%s" % servicePID)
		if isDone is False:
			servicePID = 0
			break
	except Exception as err:
		print "ERRRPR :%s" % err
		break
print 'Service off'
print 'backup log...'
#Now copy the log file

if file_name:
	import datetime
	file = 'log/%s_%s' % (file_name,port)
	new_file =  file+str(datetime.datetime.now()).replace(' ','_')
	Popen(["mv",file,new_file])
print "Starting....... server @ port: %s" % port

Popen(["python main.py " +__builtin__.mySettingFile + " &"],shell = True)

print 'Done.'
