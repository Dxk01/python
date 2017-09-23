# coding:utf-8
from django.test import TestCase

import urllib2
import json
import datetime
from MyCode import config
import codecs
import threading



class QueryTest(object):

	def __init__(self,filename="query_test"):
		self.key = config.key
		self.url = config.link_url
		self.out_file = config.QueryTestPath + "{0}_result.txt".format(filename)
		self.fp = codecs.open(self.out_file,"a+",encoding="utf-8")

	def queryTest(self,query):
		query_id = 1
		query_text = query
		print("%s : %s" % (query_id, query_text))
		try:
			start = datetime.datetime.now()

			req = urllib2.Request(self.url + urllib2.quote(query_text.encode('utf-8')))
			res_data = urllib2.urlopen(req)
			res = res_data.read()

			obj = json.loads(res)

			if True:
				hit_query = ''
				intent = ''
				if 'desc' in obj and 'textOutputDetail' in obj['desc'] and obj['desc']['textOutputDetail'] is not None:
					if 'hitQuery' in obj['desc']['textOutputDetail']:
						hit_query = obj['desc']['textOutputDetail']['hitQuery']
					if 'intent' in obj['desc']['textOutputDetail']:
						intent = obj['desc']['textOutputDetail']['intent']
				elif 'desc' in obj and 'textOutputDetail' in obj['desc'] and obj['desc']['textOutput']:
					hit_query = obj['desc']['textOutput']
				print query_id,query_text," respoense: ",hit_query
				self.fp.write("%s\t%s\t%s\t%s\t%s\r\n" % (query_id, query_text, obj['answer']['text'], intent, hit_query))
		except Exception as e:
			print e.message
			self.fp.write("%s\t%s\t%s\r\n" % (query_id, query_text, e.message))
		self.fp.close()

	def getQueriesResponse(self,queries):
		threads = []
		threads_pool = []
		threads_pool_length = 5
		result = []
		for query in queries:
			parts = query.strip()

			query = parts.strip().split("\t")
			if len(query) != 2:
				continue
			th = threading.Thread(target=self.queryTest, args=query)
			threads.append(th)

		while len(threads) > 0:
			if len(threads_pool) < threads_pool_length:
				th = threads.pop()
				threads_pool.append(th)
				th.start()
			else:
				th = threads_pool.pop(0)
				th.join()

		if len(threads_pool) > 0:
			for th in threads_pool:
				th.join()