from flask import current_app
import redis

class RedisHelper(object):

	def __init__(self, **kwargs):
		self.__pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'])
		self.__conn = redis.Redis(connection_pool=self.__pool)

	def set(self,name, value, ex=None, px=None, nx=False, xx=False):
		#可以做一些防呆設計
		#xxxxxx
		self.__conn.set(name, value, ex, px, nx, xx)

	def get(self,name):
		#可以做一些防呆設計
		#xxxxxx
		return self.__conn.get(name)

	def close(self):
		self.__pool.disconnect()
