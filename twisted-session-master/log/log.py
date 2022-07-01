from twisted.python import log
import sys
import os
import datetime
from subprocess import *
import subprocess

class Bayt_Log():
	def __init__(self):
		self.DEBUG = False
		
	def initialaizeFromSettings(self,settings):
		#TODO: when the file hits a specific size/date re-create the file again
		self.DEBUG = settings.getItem('DEBUG')
		self.file_name = settings.getItem('DEBUG_FILE')
		if self.file_name != '':
			self.file = 'log/%s_%s' % (self.file_name,settings.getItem('PORT_NUMBER'))
			log.startLogging(open(self.file, 'a'))
		else:
			log.startLogging(sys.stdout)
			self.file = ''
		self.port = settings.getItem('PORT_NUMBER')
		
				
	def logMsg(self,message,isError=False):
		if self.file != '' and os.path.exists(self.file):
			size = os.path.getsize(self.file) 
			
			if os.path.getsize(self.file) > 2000000:
				dir = 'log/%s/' % self.port
				new_file_name = '/%s_%s' % (self.file_name,self.port)
				new_file =  dir+new_file_name+str(datetime.datetime.now()).replace(' ','_')
				if os.path.exists(self.file):
					if not os.path.exists(dir):
						print 'Not Exist'
						os.makedirs(dir)
						
					Popen(["mv",self.file,new_file])
					Popen(["touch",self.file])
					log.startLogging(open(self.file, 'a'))	
				else:
					print "log file not found......log file name: %s" % self.file
		else:
			log.startLogging(sys.stdout)
			
		if self.DEBUG or isError:
			log.msg("++%s++%s" % (self.port,message) )
			
	def logError(self,command_name,error_info,originalError):
		if os.path.exists(self.file):
			size = os.path.getsize(self.file) 
		
			if os.path.getsize(self.file) > 20000000:
				dir = 'log/%s/' % self.port
				new_file_name = '/%s_%s' % (self.file_name,self.port)
				new_file =  dir+new_file_name+str(datetime.datetime.now()).replace(' ','_')
				if os.path.exists(self.file):
					if not os.path.exists(dir):
						print 'Not Exist'
						os.makedirs(dir)
						
					Popen(["mv",self.file,new_file])
					Popen(["touch",self.file])
					log.startLogging(open(self.file, 'a'))	
				else:
					print "log file not found......log file name: %s" % self.file
		else:
			log.startLogging(sys.stdout)
			
		msg = """
		===========================================
		ERROR:
		Command : %s
		Info : 
		%s
		original Error:
		%s
		===========================================		
		""" % (command_name,error_info,originalError)
		self.logMsg(msg,True)
	#def update_file(self,reactor):
		
		
bayt_log =  Bayt_Log()
__all__ = ["bayt_log"]