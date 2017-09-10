# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-08

# function  语料处理成数据

from MyCode import config
import codecs
import random

class Topic(object):
	def __init__(self):
		self.topic_id = 0
		self.topic_name = None
		self.transitionRule = None

	def setTransiTionRule(self,topic_id = None,prob = None):
		if topic_id is None or prob is None:
			return
		if self.transitionRule is None:
			self.transitionRule = {}
		self.transitionRule[topic_id] = prob

	def setTopic(self,topic_id,topic_name):
		if topic_id is None or topic_name is None:
			return
		self.topic_id = topic_id
		self.topic_name = topic_name

class TopicTransition(object):
	def __init__(self,topicFile = config.TopicFilePath + "Topic.txt",topicTran = config.TopicFilePath+"TopicTransitionRegu.txt"):
		self.TopicFile = topicFile
		self.TopicTransitionFile = topicTran
		self.Topic = None


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
				self.Topic[int(iterms[0])].setTransiTionRule(int(iterms[1]),float(iterms[2]))

	def transitionByProbility(self,topic_id):
		top = topic_id
		if type(topic_id) is not int:
			top = int(topic_id)
		pro = random.uniform(0,1)
		topic = self.Topic[top].transitionRule
		cur_pro = 0.0
		tran_topic = 0
		for rule in topic:
			cur_pro += topic[rule]
			if cur_pro >= pro:
				return rule
		return None

	def show(self):
		for top in self.Topic:
			print self.Topic[top].topic_id,self.Topic[top].topic_name
			if self.Topic[top].transitionRule is None:
				continue
			for rule in self.Topic[top].transitionRule:
				print rule,self.Topic[top].transitionRule[rule]

