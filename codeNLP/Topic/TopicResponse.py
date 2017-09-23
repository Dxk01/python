# -*- coding: utf-8 -*-

# function : get response by topic

from MyCode import config
import random
import codecs
import json


from MyCode.SentenceSimilarly.Doc2Vec import Doc2VecObj

class Sentence(object):
	def __init__(self):
		self.text = None
		self.topics = None

	def setText(self,sentence_text):
		self.text = sentence_text

	def setTopics(self,topics=["eat"]):
		self.topics = topics

	def getText(self):
		return self.text

	def getTopics(self):
		return self.topics

class Session(object):

	def __init__(self):
		self.variables = dict()

	def setVariableValue(self, key, value):
		self.variables[key] = value

	def getVariableValue(self, key):
		try:
			return self.variables[key]
		except:
			return None

class TopicResponse(object):
	""" class topic response
		to get response sentence by topic
		# if sentence not exist
		first load response sentences
	"""

	def __init__(self):
		self.topic_sentence = None
		self.ranker = None

	def load(self):
		filename = config.TopicFilePath+"topics.json"
		with codecs.open(filename,'r') as fp:
			self.topic_sentence = json.load(fp)

		# load sentence similarly model
		self.simi_Model = Doc2VecObj()
		self.simi_Model.load()

	#
	def getTopicById(self,topicId):
		topic = None
		for top in self.topic_sentence["topics"]:
			if top["id"] == topicId:
				topic = top
		return topic

	#
	def getSimilarlyQuery(self,sentence_text,topic,threshold=1.0):
		simi_query = None
		min_val = threshold

		for query in topic["query"]:
			simi_val = self.simi_Model.similarly(sentence_text,query["text"])
			if simi_val < min_val and simi_val < threshold:
				simi_query = query
				min_val = simi_val
			if abs(min_val) < 0.00000001:
				break
		return simi_query

	def getScenesRespone(self,scenes,query):
		response = None
		for responses in query['response']:
			if responses["scenesindex"] == scenes:
				response = random.choice(responses["response_text"])
		return response

	def getAgreeQuery(self,sentence_text,topic,threshold=0.5):
		response = None
		for sen in topic["agree_query"]:
			simi_val = self.simi_Model.similarly(sen,sentence_text)
			if simi_val < threshold:
				response = random.choice(topic["agree_response"])

		for sen in topic["disagree_query"]:
			simi_val = self.simi_Model.similarly(sen, sentence_text)
			if simi_val < threshold:
				response = random.choice(topic["disagree_response"])
		return response

	# 回去话题 场景下回复
	def getResponse(self,sentence,topic_id,session,topic_switched=False):
		topic = self.getTopicById(topic_id)
		if topic is None:
			return None
		# 场景解析
		scenes_index = None
		if topic_switched:
			return topic["other_topic_response"]
		else:
			scenes_index = int(session.getVariableValue('ScenesIndex'))
			if scenes_index - 1 < 0:
				return None

		# 相似query 匹配 更具相似query 获取场景回复
		query = self.getSimilarlyQuery(sentence.text,topic,threshold=1.0)
		response = None
		if query:
			response = self.getScenesRespone(scenes=scenes_index,query=query)
		else:
			response = self.getAgreeQuery(sentence.text,topic)
		return response

if __name__ == '__main__':
	tr = TopicResponse()
	tr.load()
	sentence = Sentence()
	sentence.setText(u"好呀")
	sentence.setTopics(["eat"])
	session = Session()
	session.setVariableValue("ScenesIndex",2)
	topicId = 1
	print tr.getResponse(sentence,topicId,session)

