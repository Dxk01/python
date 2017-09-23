# -*- coding: utf-8 -*-
# function : topic
import random

from TopicResponse import TopicResponse
from TopicSwitch import TopicSwitch

session = {
	"res_condition":1,
	'preQueryTopic':None,
	'preResponseTopic':None
}

class Sentence(object):
	def __init__(self):
		self.text = None
		self.topics = ['eat']
		self.switchTopics = ['eat','work','cloth']


class TopicAnalysis(object):
	def __init__(self):
		self.sentenceTag = None
		self.TopicTransition = None
		self.TopicResponse = None
		self.load()

	def load(self):
		self.TopicSwitch = TopicSwitch()
		self.TopicResponse = TopicResponse()
		# self.sentenceTag = SentenceTopicTag()

	def getResponse(self, sentence, session, scenario=None, user=None, personas=None, history=None, topic_name=None):
		# 标记query的话题类别,并获取转移话题的话题ID
		topic = topic_name
		if topic is None or len(topic) == 0:
			if session['preResponseTopic'] == None:
				topic = session['preQueryTopic']
			else:
				topic = session['preResponseTopic']

		if topic is None or len(topic) == 0:
			return None

		# 记录 query pair topic
		session['preQueryTopic'] = topic
		topic_id = self.TopicSwitch.getTopicId(topic)
		topic_id = self.TopicSwitch.transitionByProbility(topic_id)
		if topic_id:
			session['preResponseTopic'] = self.TopicSwitch.getTopic(topic_id)
		else:
			return None

		# 获得转移话题的回复sentence
		text_out = self.TopicResponse.getResponse(topic_id,session)
		return text_out

	""" 
		判断 话题转换 是否有数据，
		如果有待转换话题，则根据话题队列随机转换话题
		否则返回None 使用原query 转换话题
	"""
	def topicSwitch(self,switch_topics):
		if len(switch_topics) < 1:
			return None

		if len(switch_topics) == 1:
			return self.TopicTransition.getTopicId(switch_topics[0])

		nums = len(switch_topics)
		pro = random.uniform(0,1)
		cur_pro = 1.0/nums
		i = 0
		while cur_pro < pro:
			cur_pro += 1.0/nums
			i += 1
		return self.TopicTransition.getTopicId(switch_topics[i])


def main():
	Ta = TopicAnalysis()
	sentence = Sentence()
	print Ta.getResponse(sentence,session,topic_name="eat")

if __name__ == '__main__':
	main()



