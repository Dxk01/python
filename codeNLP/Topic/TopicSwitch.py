# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-08

# function  语料处理成数据

from MyCode import config
import codecs
import random

class Topic(object):

	""" class of Topic struct"""
	def __init__(self):
		self.topic_id = 0
		self.topic_name = None
		self.transitionRule = None

	"""  init Topic """
	def setTransiTionRule(self,topic_id = None,prob = None):
		if topic_id is None or prob is None:
			return
		if self.transitionRule is None:
			self.transitionRule = {}
		self.transitionRule[topic_id] = prob

	""" init topic trans rule """
	def setTopic(self,topic_id,topic_name):
		if topic_id is None or topic_name is None:
			return
		self.topic_id = topic_id
		self.topic_name = topic_name

class TopicSwitch(object):
	""" topic transition """
	def __init__(self,topicFile = config.TopicFilePath + "Topic.txt",topicTran = config.TopicFilePath+"TopicTransitionRegu.txt"):
		self.TopicFile = topicFile
		self.TopicTransitionFile = topicTran
		self.load()

	""" load topic """
	def load(self):
		# 加载话题字典，映射话题和相应的ID
		self.Topic = {}
		with codecs.open(self.TopicFile,'r',encoding="utf-8") as fp:
			for line in fp:
				iterms = line.strip().split(":")
				tp = Topic()
				tp.setTopic(int(iterms[0]),iterms[1])
				self.Topic[int(iterms[0])] = tp
		# 加载话题跳转规则
		with codecs.open(self.TopicTransitionFile,'r',encoding="utf-8") as fp:
			for line in fp:
				iterms = tuple(line.strip().split(","))
				if len(iterms) != 3:
					continue
				if int(iterms[0]) not in self.Topic:
					self.Topic[int(iterms[0])] = Topic()
				self.Topic[int(iterms[0])].setTransiTionRule(int(iterms[1]),float(iterms[2]))

	""" topic transition """
	""" 
		判断 话题转换 是否有数据，
		如果有待转换话题，则根据话题队列随机转换话题
		否则返回None 使用原query 转换话题
	"""
	def transitionByProbility(self,topic_id):
		top = int(topic_id)
		pro = random.uniform(0,1)
		if top not in self.Topic:
			return None
		topic = self.Topic[top].transitionRule
		if topic == None or len(topic) == 0:
			return None
		cur_pro = 0.0
		tran_topic = 0
		for rule in topic:
			cur_pro += topic[rule]
			if cur_pro >= pro:
				return rule
		return None

	""" get topic name by topic_id """
	def getTopic(self,topic_id):
		if topic_id not in self.Topic:
			return None
		return self.Topic[topic_id].topic_name

	""" get topic Id by topic name """
	def getTopicId(self,topicname):
		topic_id = None
		for topic in self.Topic:
			if self.Topic[topic].topic_name == topicname:
				return topic

	def show(self):
		for top in self.Topic:
			print self.Topic[top].topic_id,self.Topic[top].topic_name
			if self.Topic[top].transitionRule is None:
				continue
			for rule in self.Topic[top].transitionRule:
				print rule,self.Topic[top].transitionRule[rule]

