from subprocess import *

from Settings.active_servers import *
for file in active_servers_settings_files:
	print "1>><< %s" % file
	Popen(["python server_res.py %s" % file ],shell = True)
#class simpleClient(basic.LineReceiver):   
#	def connectionMade(self):
#
#		cmdPacket = '[{"cmd" : "shutdown","bayt_user" : "'+user+'","user_pass" : "'+password+'","vars" : "[{\\"X\\" : \\"X\\"}]"}]'
#		self.transport.write(cmdPacket+"\r\n")
#	
#	def dataReceived(self, data):
#		self.factory.servicePID = data
#
#		self.transport.loseConnection()
#	
#	def connectionLost(self, reason):
#		reactor.stop()
#
#class simpleClientFactory(protocol.ClientFactory):
#	protocol = simpleClient	
#	servicePID = 0
#
#def runMain():
#	Popen('python','main.py')
#
#
#
#print 'Send safe shutdown....'
#fact = simpleClientFactory()
#reactor.connectTCP('localhost', port, fact)
#reactor.callLater(5,reactor.stop)
#reactor.run()
#reactor.callLater(5,reactor.stop)
#servicePID = fact.servicePID
#while servicePID != 0 :
#	isDone = ''
#	p1 = Popen(["ps","-e"], stdout=PIPE)
#	p2 = Popen(["awk", "{print $1}"], stdin=p1.stdout, stdout=PIPE)
#	p3 = Popen(["grep",str(servicePID)], stdin=p2.stdout, stdout=PIPE)
#	try:
#		p1.stdout.close()
#		p2.stdout.close()
#		isDone = p3.communicate()[0]	   
#		if isDone == '':
#			servicePID = 0		
#	except Exception as err:
#		#Its possible that while reading the process list , the pipe get close due to the process kill
#		pass
#print 'Service off'
#print 'backup log...'
##Now copy the log file
#
#if file_name:
#	import datetime
#	file = 'log/%s' % file_name 
#	new_file =  file+str(datetime.datetime.now()).replace(' ','_')
#	Popen(["mv",file,new_file])
#print 'Starting.......'
#
#Popen(["python main.py &"],shell = True)
#
#print 'Done.'
#
		