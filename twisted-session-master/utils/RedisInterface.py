"""
@file protocol.py

@author Reza Lotun (rlotun@gmail.com)
@date 06/22/10
Added multi-bulk command sending support.
Added support for hash commands.
Added support for sorted set.
Added support for new basic commands APPEND and SUBSTR.
Removed forcing of float data to be decimal.
Removed inlineCallbacks within protocol code.
Added setuptools support to setup.py

@author Garret Heaton (powdahound@gmail.com)
@date 06/15/10
Added read buffering for bulk data.
Removed use of LineReceiver to avoid Twisted recursion bug.
Added support for multi, exec, and discard

@author Dorian Raymer
@date 02/01/10
Added BLPOP/BRPOP and RPOPLPUSH to list commands.
Added doc strings to list commands (copied from the Redis google code
project page).

@author Dorian Raymer
@author Ludovico Magnocavallo
@date 9/30/09
@brief Twisted compatible version of redis.py

@mainpage

txRedis is an asynchronous, Twisted, version of redis.py (included in the
redis server source).

The official Redis Command Reference:
http://code.google.com/p/redis/wiki/CommandReference

@section An example demonstrating how to use the client in your code:
@code	clientCreator = protocol.ClientCreator(reactor, Redis)
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import defer

from txredis.protocol import Redis

@defer.inlineCallbacks
def main():
	clientCreator = protocol.ClientCreator(reactor, Redis)
	redis = yield clientCreator.connectTCP(HOST, PORT)

	res = yield redis.ping()
	print res

	res = yield redis.set('test', 42)
	print res

	test = yield redis.get('test')
	print res

@endcode

Redis google code project: http://code.google.com/p/redis/
Command doc strings taken from the CommandReference wiki page.

"""


from collections import deque
from itertools import chain, izip

from twisted.internet import defer, protocol
from twisted.protocols import policies

from twisted.internet import defer
from log.log import *
from utils.commandsClient.ERRORS import *
from utils.RedisInterface import *
from twisted.internet import reactor, defer
from Settings.settings_manager import *
import __builtin__
__builtin__.mySettingFile = 'Settings/server1_settings.py'


try:
	import hiredis
except ImportError:
	pass

class RedisError(Exception):
	pass


class ConnectionError(RedisError):
	pass


class ResponseError(RedisError):
	pass


class InvalidResponse(RedisError):
	pass


class InvalidData(RedisError):
	pass


class RedisBase(protocol.Protocol, policies.TimeoutMixin, object):
	"""The main Redis client."""	
	ERROR = "-"
	SINGLE_LINE = "+"
	INTEGER = ":"
	BULK = "$"
	MULTI_BULK = "*"

	def __init__(self, db=None, password=None, charset='utf8', errors='strict'):		
		self.charset = charset
		self.db = db if db is not None else 0
		self.password = password
		self.errors = errors
		self._buffer = ''
		self._bulk_length = None
		self._disconnected = False
		self._multi_bulk_length = None
		self._multi_bulk_reply = []
		self._request_queue = deque()
		
		
	def dataReceived(self, data):
		"""Receive data.

		Spec: http://redis.io/topics/protocol
		"""		
		self.resetTimeout()
		self._buffer = self._buffer + data

		while self._buffer is not None or self._buffer != '':			
			# if we're expecting bulk data, read that many bytes
			if self._bulk_length is not None:
				# wait until there's enough data in the buffer
				if len(self._buffer) < self._bulk_length + 2: # /r/n
					return
				data = self._buffer[:self._bulk_length]
				self._buffer = self._buffer[self._bulk_length+2:] # 2 for /r/n
				self.bulkDataReceived(data)
				continue

			# wait until we have a line
			if '\r\n' not in self._buffer:
				return

			# grab a line
			line, self._buffer = self._buffer.split('\r\n', 1)
			if len(line) == 0:
				continue

			# first byte indicates reply type
			reply_type = line[0]
			reply_data = line[1:]

			# Error message (-)
			if reply_type == self.ERROR:
				self.errorReceived(reply_data)
			# Integer number (:)
			elif reply_type == self.INTEGER:
				self.integerReceived(reply_data)
			# Single line (+)
			elif reply_type == self.SINGLE_LINE:
				
				self.singleLineReceived(reply_data)
			# Bulk data (&)
			elif reply_type == self.BULK:
				try:
					self._bulk_length = int(reply_data)
				except ValueError:
					r = InvalidResponse("Cannot convert data '%s' to integer"
						% reply_data)
					self.responseReceived(r)
					return
				# requested value may not exist
				if self._bulk_length == -1:
					self.bulkDataReceived(None)
			# Multi-bulk data (*)
			elif reply_type == self.MULTI_BULK:
				# reply_data will contain the # of bulks we're about to get
				try:
					self._multi_bulk_length = int(reply_data)
				except ValueError:
					r = InvalidResponse("Cannot convert data '%s' to integer"
						% reply_data)
					self.responseReceived(r)
					return
			if self._multi_bulk_length == -1:
				self._multi_bulk_reply = None
				self.multiBulkDataReceived()
				return
			elif self._multi_bulk_length == 0:
				self.multiBulkDataReceived()
	
	def failRequests(self, reason):		
		while self._request_queue:
			d = self._request_queue.popleft()			
			d.errback(reason)

	def connectionMade(self):	
		d = defer.succeed(True)
		# if we have a password set, make sure we auth
		if self.password:			
			d.addCallback(lambda _res : self.auth(self.password))

		# select the db passsed in
		if self.db:			
			d.addCallback(lambda _res : self.select(self.db))

		def done_connecting(_res):			
			# set our state as soon as we're properly connected
			self._disconnected = False
			
		d.addCallback(done_connecting)	
		return d

	def connectionLost(self, reason):
		self._disconnected = True
		self.failRequests(reason)

	def timeoutConnection(self):
		"""Called when the connection times out.

		Will fail all pending requests with a TimeoutError.

		"""
		self.failRequests(defer.TimeoutError("Connection timeout"))
		self.transport.loseConnection()

	def errorReceived(self, data):
		reply = ResponseError(data if data[:4] == 'ERR ' else data)
		if self._request_queue:
			# properly errback this reply
			self._request_queue.popleft().errback(reply)
		else:
			# we should have a request queue - if not, just raise this exception
			raise reply

	def singleLineReceived(self, data):
		"""Single line response received."""
		if data == 'none':
			reply = None # should this happen here in the client?
		else:
			reply = data

		self.responseReceived(reply)

	def handleMultiBulkElement(self, element):
		self._multi_bulk_reply.append(element)
		self._multi_bulk_length = self._multi_bulk_length - 1
		if self._multi_bulk_length == 0:
			self.multiBulkDataReceived()

	def integerReceived(self, data):		
		"""Integer response received."""
		try:
			reply = int(data)
		except ValueError:
			reply = InvalidResponse("Cannot convert data '%s' to integer"
				% data)
		if self._multi_bulk_length > 0:
			self.handleMultiBulkElement(reply)
			return

		self.responseReceived(reply)
		
	def bulkDataReceived(self, data):
		"""Bulk data response received."""
		self._bulk_length = None
		self.responseReceived(data)

	def multiBulkDataReceived(self):
		"""Multi bulk response received.

		The bulks making up this response have been collected in
		self._multi_bulk_reply.

		"""
		reply = self._multi_bulk_reply
		self._multi_bulk_reply = []
		self._multi_bulk_length = None
		self.handleCompleteMultiBulkData(reply)

 
	def handleCompleteMultiBulkData(self, reply):
		self.responseReceived(reply)

	def responseReceived(self, reply):
		"""Handle a server response.

		If we're waiting for multibulk elements, store this reply. Otherwise
		provide the reply to the waiting request.

		"""
		if self._multi_bulk_length > 0:
			self.handleMultiBulkElement(reply)
		elif self._request_queue:	
			self._request_queue.popleft().callback(reply)

	def getResponse(self):		
		"""
		@retval a deferred which will fire with response from server.
		"""
		if self._disconnected:
			return defer.fail(RuntimeError("Not connected"))

		d = defer.Deferred()
		self._request_queue.append(d)
		return d

	def _encode(self, s):
		"""Encode a value for sending to the server."""
		if isinstance(s, str):
			return s
		if isinstance(s, unicode):
			try:
				return s.encode(self.charset, self.errors)
			except UnicodeEncodeError, e:
				raise InvalidData("Error encoding unicode value '%s': %s"
					% (s.encode(self.charset, 'replace'), e))
		return str(s)

	def _send(self, *args):		
		"""Encode and send a request using the 'unified request protocol' (aka multi-bulk)"""
		cmds = []
		for i in args:
			v = self._encode(i)
			cmds.append('$%s\r\n%s\r\n' % (len(v), v))
		cmd = '*%s\r\n' % len(args) + ''.join(cmds)
		self.transport.write(cmd)

	def send(self, command, *args):
		self._send(command, *args)
		return self.getResponse()
	


	
	
	
class twisted_redis_class():	
	def __init__(self,host,port):		
		self.HOST =  host#settingsm.getItem('REDIS_HOST')
		self.PORT =  port #
		self.RedisclientCreator = protocol.ClientCreator(reactor, RedisBase)
		self.redis = None
		self.redis_init = 0

	
	def _internalSend(self, *args):	
		
		if self.redis_init == 0:			
			self.redis = args[0]
			self.redis_init = 1
		
		self.redis._send(*args[1])
		return self.redis.getResponse()
	
	def CloseConnection(self):
		if self.redis is not None:
			self.redis.transport.loseConnection()

	def Redisfull_send(self, *args):		
		if self.redis is None:		
			d = self.RedisclientCreator.connectTCP(self.HOST,self.PORT)	
		else :
			if self.redis._disconnected:
				self.redis_init = 0
				d = self.RedisclientCreator.connectTCP(self.HOST, self.PORT)
			else:
				d = defer.Deferred()
				d.called = True
				d.result = None
		d.addCallback(self._internalSend, args)
		return d

	
	
	
	
class twisted_redis_class_auto_close():	
	def __init__(self,host,port):		
		self.HOST =  host#settingsm.getItem('REDIS_HOST')
		self.PORT =  port #
		self.RedisclientCreator = protocol.ClientCreator(reactor, RedisBase)
		self.redis = None
		self.redis_init = 0

	def _internalSend(self, *args):	
		if self.redis_init == 0:			
			self.redis = args[0]
			self.redis_init = 1
		self.redis._send(*args[1])
		return self.redis.getResponse()
		
	
	
	def CloseConnection(self,*args):
		self.redis.transport.loseConnection()
		return args[0]

	def Redisfull_send(self, *args):
		d = defer.Deferred()		
		if self.redis is None:		
			d.addCallback(self.connect)
		else :
			if self.redis._disconnected:
				self.redis_init = 0
				d.addCallback(self.connect)
		drf = d.addCallback(self._internalSend, args)
		drf.addCallback(self.CloseConnection)
		return drf
	
	def connect(self,*args):
		return self.RedisclientCreator.connectTCP(self.HOST,self.PORT)	

	

class sessionsViewCache_updated(twisted_redis_class_auto_close):
	def __init__(self):
		twisted_redis_class_auto_close.__init__(self,settingsm.getItem('sessionsViewCache_REDIS_HOST'),settingsm.getItem('sessionsViewCache_REDIS_PORT_NUMBER'))

class userViewCache_updated(twisted_redis_class_auto_close):
	def __init__(self):
		twisted_redis_class_auto_close.__init__(self,settingsm.getItem('userViewCache_REDIS_HOST'),settingsm.getItem('userViewCache_REDIS_PORT_NUMBER'))	
	
	
class sessionsViewCache(twisted_redis_class):
	def __init__(self):
		twisted_redis_class.__init__(self,settingsm.getItem('sessionsViewCache_REDIS_HOST'),settingsm.getItem('sessionsViewCache_REDIS_PORT_NUMBER'))

class userViewCache(twisted_redis_class):
	def __init__(self):
		twisted_redis_class.__init__(self,settingsm.getItem('userViewCache_REDIS_HOST'),settingsm.getItem('userViewCache_REDIS_PORT_NUMBER'))		
	
class sessionsViewReadCache_updated(twisted_redis_class_auto_close):
	def __init__(self):
		twisted_redis_class_auto_close.__init__(self,settingsm.getItem('sessionsViewReadCache_REDIS_HOST'),settingsm.getItem('sessionsViewReadCache_REDIS_PORT_NUMBER'))
		
class sessionsViewReadCache(twisted_redis_class):
	def __init__(self):
		twisted_redis_class.__init__(self,settingsm.getItem('sessionsViewReadCache_REDIS_HOST'),settingsm.getItem('sessionsViewReadCache_REDIS_PORT_NUMBER'))
	
__all__ = ["sessionsViewCache", "userViewCache", "sessionsViewCache_updated", "userViewCache_updated", "sessionsViewReadCache", "sessionsViewReadCache_updated"]

