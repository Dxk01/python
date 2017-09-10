# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-09

from MyCode import config
from MyCode.tools import ReadFile
from MyCode.Algorithm.HDA import HDA
from TopicTransition import Topic
from TopicTransition import TopicTransition
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
		doc_topic = self.model.getTopicLab(sentence)
		if doc_topic[1] > 0.75:
			sentence.topics = [doc_topic[0]]
