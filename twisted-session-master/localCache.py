from utils.RedisInterface import userViewCache
from twisted.internet import defer
class bccIDsCache:
	bccs_Cache = {}
	@staticmethod
	def add_new_bcc(bcc_id):		
		if not bccIDsCache.bccs_Cache.has_key(bcc_id):
			bccIDsCache.bccs_Cache[bcc_id] = bcc_id
			redis_instance2   = userViewCache()
			d = redis_instance2.Redisfull_send("HSET","BCC_IDS_FOR_SESSIONS_BY_USER",bcc_id,"1")
			def cleanRedisConnection(*args):
				redis_instance2.CloseConnection()
			d.addCallback(cleanRedisConnection)
			return d
		return None
	@staticmethod
	def remove_bcc(bcc_id):
		if bccIDsCache.bccs_Cache.has_key(bcc_id):
			bccIDsCache.bccs_Cache.pop(bcc_id)
			redis_instance2   = userViewCache()
			d = redis_instance2.Redisfull_send("HDEL","BCC_IDS_FOR_SESSIONS_BY_USER",bcc_id)
			def cleanRedisConnection(*args):
				redis_instance2.CloseConnection()
			d.addCallback(cleanRedisConnection)
			return d
		return None		

		
	@staticmethod
	def get_all_bcc_ids():
		return bccIDsCache.bccs_Cache.keys()
	
	@staticmethod
	def load_from_redis():
		redis_instance2   = userViewCache()
		d = redis_instance2.Redisfull_send("HKEYS","BCC_IDS_FOR_SESSIONS_BY_USER")
		def fill_me(*args):
			if args[0] is not None:
				for k in args[0]:
					bccIDsCache.bccs_Cache[k] = k
			redis_instance2.CloseConnection()

		d.addCallback(fill_me)	
		return d
		