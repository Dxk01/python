# encoding: utf-8
"""
作者：liguoyu
"""
import time
from http import cookiejar

import requests
from bs4 import BeautifulSoup
import json
from Login import Login
from MyCode import config
import codecs

class SpiderTopicData(object):
	"""
	获取知乎数据
	"""
	def __init__(self):
		"""
		初始化相关参数
		"""
		self.login = Login()
		self.login.login()
		self.headers = self.login.getHeaders()
		self.data = self.login.getData()
		self.session = self.login.getSession()
		# self.session.encoding = 'utf8'
		# print self.session.
		# data link list
		self.havefinished_list = []   # 已经处理的数据连接
		self.waitting_list = []       # 未处理的数据连接
		self.record_topic_data = dict()
		self.record_topic_link_data = dict()

	def setRootTopic(self,root_topic_id='19778317'):
		self.waitting_list.append(root_topic_id)

	def relogin(self):
		"""
		短线重连
		:return:
		"""
		self.login.login()
		self.headers = self.login.getHeaders()
		self.data = self.login.getData()
		self.session = self.login.getSession()

	def getLinkTopic(self,link_url='https://www.zhihu.com/topic/19778317/organize/entire?parent=19778317'):
		"""
		获取连接下的数据
		:param link_url:
		:return: 数据 text
		"""
		# self.session
		try:
			res = self.session.post(link_url,data=self.data,headers=self.headers)
		except:
			self.relogin()
			res = self.session.post(link_url,data=self.data,headers=self.headers)
		topic = json.loads(res.text)
		# topic = eval(res.text)
		cur_topic = topic['msg'][0]
		sub_topics = topic['msg'][1]
		# for test
		parent_topic_name = cur_topic[1].encode('utf8')
		parent_topic_id = cur_topic[2]
		sub_topics_name = []
		sub_topics_id = []
		for sub in sub_topics:
			sub_topics_id.append(sub[0][2])
			sub_topics_name.append(sub[0][1].encode('utf8'))
		result = dict()
		result["parent_topic_id"] = parent_topic_id
		result["parent_topic_name"] = parent_topic_name
		result["sub_topics_name"] = sub_topics_name
		result["sub_topics_id"] = sub_topics_id
		return result

	def recordData(self,result):
		"""
		处理爬取的topic 数据，并记录
		:param result:
		:return:
		"""
		sub_topics_id = result['sub_topics_id']
		sub_topics_name = result['sub_topics_name']
		parent_topic_name = result['parent_topic_name']
		parent_topic_id = result['parent_topic_id']
		existed = False
		child_topic_id = ''
		if parent_topic_id not in self.record_topic_data:
			self.record_topic_data[parent_topic_id] = parent_topic_name
		for sub_id,sub_name in zip(sub_topics_id,sub_topics_name):
			if sub_name == str("加载更多"):
				existed = True
				child_topic_id = sub_id
				continue
			if sub_id not in self.record_topic_data:
				self.record_topic_data[sub_id] = sub_name
			if sub_id not in self.record_topic_link_data:
				self.record_topic_data[sub_id] = []
			self.record_topic_data[sub_id].append(parent_topic_id)
		return existed,parent_topic_id,child_topic_id

	def getSubTopic(self,parent_topic_id='19778317',child_topic_id=''):
		"""
		爬取知乎某一话题下的所有子话题，仅爬取话题下一层（即仅爬取当前话题的孩子话题，孙子不管）
		:param parent_topic_id: 当前话题 ID
		:param child_topic_id: 子话题 ID应对显示不全时
		:return:
		"""
		state = True
		sub_topics_id = []
		while state:
			url_link = 'https://www.zhihu.com/topic/{0}/organize/entire'.format(parent_topic_id)
			if child_topic_id:
				url_link += "?child={}&parent={}".format(child_topic_id, parent_topic_id)
			result = self.getLinkTopic(url_link)
			sub_topics_id.extend(result['sub_topics_id'])
			state,parent_topic_id,child_topic_id = self.recordData(result)
		return sub_topics_id


	def getAllTopic(self):
		"""
		爬取队列所有话题及子话题
		:return:
		"""
		while self.waitting_list:
			topic_id = self.waitting_list.pop(0)
			if topic_id in self.havefinished_list:
				continue
			sub_topics = self.getSubTopic(parent_topic_id=topic_id)
			self.waitting_list.extend((list(set(sub_topics))))
			self.havefinished_list.append(topic_id)
			time.sleep(5)

	def writeResulttoFile(self,topic_file=config.TopicFilePath+"zhihu_topic.txt",topic_link_file = config.TopicFilePath+'zhihu_topic_link.txt'):
		with codecs.open(topic_file,'w') as topic_fp:
			json.dump(self.record_topic_data,topic_fp)

		with codecs.open(topic_link_file,'w') as topic_link_fp:
			json.dump(self.record_topic_link_data,topic_link_fp)


def main():
	spiderData = SpiderTopicData()
	spiderData.setRootTopic()
	# result = spiderData.getLinkTopic()
	# spiderData.recordData(result)
	# spiderData.getSubTopic()
	spiderData.getAllTopic()
	spiderData.writeResulttoFile()
	# print set(spiderData.waitting_list)
	# print len(spiderData.waitting_list)

if __name__ == "__main__":
	main()