from pkgutil import iter_modules
import inspect

from utils.commandsClient.baytCommand import bayt_command
from log.log import *
import sys
class baytCommands():
	def __init__(self):
		self._modules = {}
		self._serviceCommands = self._load_commands()
	def _isvalidCommandFile(self,obj):
		if inspect.isclass(obj) and issubclass(obj, bayt_command)  and getattr(obj, 'CMDName', False) and getattr(obj, 'preWrite', False) and getattr(obj, 'postWrite', False)  :	
			return True
		else:
			return False  
		
	def ReLoadCommandFile(self,name):
		clas = self.getCommandbyName(name)
		if clas:
			module  = reload(sys.modules[clas.__module__])
			if module:
				for obj in vars(module).itervalues():
					if self._isvalidCommandFile(obj) and getattr(obj, 'CMDName','') != 'reload':
					   self._serviceCommands[obj.CMDName] =  obj
					   return True
		else:
			#New One
			for module in self._walkModules('baytCommands'):
				for obj in vars(module).itervalues():
					if name == getattr(obj, 'CMDName','') and self._isvalidCommandFile(obj) and  getattr(obj, 'CMDName','' != 'reload'):
					   self._serviceCommands[obj.CMDName] =  obj
					   return True			
		return False
		
	def readNewCommands(self):
		 self._serviceCommands = self._load_commands(False)  
	
	def getCommandNames(self):
		return self._serviceCommands.keys()
	
	def getCommandbyName(self,name):
		return self._serviceCommands.get(name)
	
	def getCommandObjectByName(self,name):
		clas = self.getCommandbyName(name)
		if clas is not None:
			return clas()
		else:
			return None
		
	def _load_commands(self,load_reload = True):

		commands = {}
		
		for module in self._walkModules('baytCommands'):
			for obj in vars(module).itervalues():
				if self._isvalidCommandFile(obj) and (load_reload or getattr(obj, 'CMDName','') != 'reload'):
				   commands[obj.CMDName] =  obj
		return commands			   
	
	def _walkModules(self,path):
		"""Loads a module and all its submodules from a the given module path and
		returns them. If *any* module throws an exception while importing, that
		exception is thrown back.
		""" 
		mods = []
		mod = __import__(path, {}, {}, [''])
		mods.append(mod)
		if hasattr(mod, '__path__'):
			for _, subpath, ispkg in iter_modules(mod.__path__):
				fullpath = ""
				fullpath = path + '.' + subpath
				if ispkg:
					mods += self._walkModules(fullpath)
				else:
					submod = __import__(fullpath, {}, {}, [''])
					mods.append(submod)
		return mods

serviceCommands = baytCommands()	
			
__all__ = ["serviceCommands"]
	 
