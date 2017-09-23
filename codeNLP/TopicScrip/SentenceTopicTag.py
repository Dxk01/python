# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-09

from MyCode import config
from MyCode.tools import ReadFile
from MyCode.Algorithm.HDA import HDA
from MyCode.Topic.TopicSwitch import Topic
from MyCode.Topic.TopicSwitch import TopicTransition
from MyCode.Struct.Sentence import Sentence

class SentenceTopicTag(object):
	" class for tag topic of sentence "

	"""
		:param 
		model can be LDA or HDA model
	
	"""
	def __init__(self):
		Lda_topic = HDA("test_Hda", "test_Hda_word")
		Lda_topic.load_word_dic()
		Lda_topic.load_HDAModel()
		self.model = Lda_topic
		self.topic = TopicTransition()
		self.topic.load()

	def tagTopic(self,sentence):
		doc_topic = self.model.getTopicLab(sentence.text)
		topic_id = None
		if doc_topic[1] > 0.8:
			topic_id = doc_topic[0]
		sentence.topics.append(self.topic.getTopic(topic_id))
		return topic_id

	def tranTopicodSentence(self,sentence):
		if sentence.text == "":
			return None

		if sentence.topics == None:
			sentence.topics = []
		topic_id = None
		if len(sentence.topics) == 0:
			topic_id = self.tagTopic(sentence)

		if topic_id == None:
			return None

		tran_Topic = self.topic.transitionByProbility(topic_id)
		return tran_Topic




