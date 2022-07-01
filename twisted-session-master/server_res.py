import sys
import __builtin__
__builtin__.mySettingFile = 'Settings/server1_settings.py'
if (len(sys.argv) > 1):
	__builtin__.mySettingFile = "Settings/"  + sys.argv[1] 
	



from subprocess import *
import os
from Settings.settings_manager import *
from twisted.internet import reactor , protocol
from twisted.protocols import basic
import subprocess

port  = settingsm.getItem('PORT_NUMBER')
user = settingsm.getItem('USER')
password =  settingsm.getItem('PASSWORD')
file_name = settingsm.getItem('DEBUG_FILE')

class simpleClient(basic.LineReceiver):   
	def connectionMade(self):
		cmdPacket = "shutdown?bayt_user="+user+"&user_pass="+password
		self.transport.write(cmdPacket+"\r\n")
	
	def dataReceived(self, data):
		self.factory.servicePID = data
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
	dir = 'log/%s/' % port
	new_file_name = '/%s_%s' % (file_name,port)
	new_file =  dir+new_file_name+str(datetime.datetime.now()).replace(' ','_')
	if os.path.exists(file):
		if not os.path.exists(dir):
			print 'Not Exist'
			os.makedirs(dir)
		Popen(["mv",file,new_file])	
	else:
		print "log file not found......log file name: %s" % file
		
print "Starting....... server @ port: %s" % port

Popen(["python main.py " +__builtin__.mySettingFile + " &"],shell = True)

print 'Done.'

