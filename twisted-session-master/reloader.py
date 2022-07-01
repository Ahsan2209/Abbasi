from subprocess import *

import sys
import __builtin__
if (len(sys.argv) > 1):
	file_name = sys.argv[1]
else:
	print "ERROR: Enter the desired file name"
	
	
from Settings.active_servers import *
for file in active_servers_settings_files:
	print "1>><< %s" % file
	Popen(["python server_rel.py %s %s" % (file,file_name)],shell = True)