class settingsManager():
	def __init__(self,defaultFile='Settings/default_settings.py',settingsFile='settings.py',local=False):
		import os
		import os.path
		import ConfigParser
		import io
		if not os.path.exists(defaultFile) :
			print 'ERROR While Loading: File %s NOT FOUND' % defaultFile
			if local:
				import sys
				sys.exit()
			else :
				return
		
		#LOAD DEAFULT FILE
		config = ConfigParser.RawConfigParser()
		file = open(defaultFile,'rb')
		default_lines = file.readlines()
		default_lines = ''.join(default_lines)
		file.close()
		default_lines = '[Default]\n%s' % default_lines
		
		#LOAD SETTINGS FILE
		if os.path.exists(settingsFile) :
			file = open(settingsFile,'rb')
			conf_lines = file.readlines()
			conf_lines = ''.join(conf_lines)
			file.close()
		else :
			conf_lines = ''
		
		#CREATE temp config File
		conf_lines = '[CONF]\n%s' % conf_lines
		lines = "%s\n%s" % (default_lines,conf_lines)	 
		config.readfp(io.BytesIO(lines))
		#Extract names from temp config file
		values = config.items('CONF')
		default = config.items('Default')
		self.values = {}
		#Start 
		for value in values:
			self.values[value[0]] = self._parse(value[1])
		for defaultValue in default:
		   if self.values.has_key(defaultValue[0]) is not None:
			   self.values[defaultValue[0]] = self._parse(defaultValue[1])
	   
				
	def _parse(self,value):
		code = 'key = %s' % value
		try:
			exec code
		except :
			return None
		return key
	def getItem(self,itemName):
		str(itemName).lower()
		return self.values.get(str(itemName).lower())
	

if __name__ == "__main__":
	settingsm = settingsManager(local=True,defaultFile='default_settings.py')
	print "--------------------------------------------------------"
	for key in settingsm.values:
		print '%-30s | %15s'  % (key,str(settingsm.values.get(key)))
		print "-------------------------------|--------------------"
else :
	import __builtin__
	settingsm = settingsManager(__builtin__.mySettingFile)
	_all_ = ["settingsm"]
	
