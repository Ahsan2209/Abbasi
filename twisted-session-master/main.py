import sys
import __builtin__
__builtin__.mySettingFile = 'Settings/server1_settings.py'
if (len(sys.argv) > 1):
	__builtin__.mySettingFile = sys.argv[1] 

from twisted.internet import reactor
from log.log import * 
from BaytLoader import BaytLoader
from BaytFactory import baytFactory
from twisted.application import internet, service

#Load All modules
loader  = BaytLoader()
factory =  baytFactory(loader.getmaxNumberOfConnecion(),loader.get_userName(),loader.get_password(),reactor)
iis = reactor.listenTCP(loader.getPort(),factory)
factory.iis = iis
reactor.run()