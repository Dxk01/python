# encoding: utf-8
"""
作者：liguoyu
"""
import sys
sys.path.append("../")
sys.path.append('../../')
reload(sys)
import time
from MyCode import config
import random
from SpiderTopicQuestions import SpiderTopicQuestions
from TopicTree import TopicTree
import pickle


class SpiderData(object):
	""" 批量爬取 多个话题的 批量的问题数据 并标记 问题的话题ID """
	def __init__(self, spider_number=2000, savefile=config.TopicFilePath+"topic_questions_v2.csv"):
		topictree = TopicTree()
		topictree.paserData(data=topictree.load(config.TopicFilePath+'zhihu_topic_link_1.json'))

		self.topics = topictree.getDeepTopic()
		self.finished_topic = []

		self.spider_topic_questions = SpiderTopicQuestions()
		self.spider_topic_questions.setQuestions_number(spider_number)
		self.spider_topic_questions.setSaveFile(file=savefile)

	def spider(self):
		while self.topics:
			topic = self.topics.pop(0)
			self.spider_topic_questions.Spider(topic)
			self.finished_topic.append(topic)
			self.record()

	def record(self):
		with open(config.TopicFilePath+"questionTopic_wait.txt",'wb') as fp:
			pickle.dump(self.topics,fp)

		with open(config.TopicFilePath+"questionTopic_fini.txt",'wb') as fp:
			pickle.dump(self.finished_topic,fp)

	def loadRecord(self):
		with open(config.TopicFilePath + "questionTopic_wait.txt", 'rb') as fp:
			self.topics = pickle.load(fp)

		with open(config.TopicFilePath + "questionTopic_fini.txt", 'rb') as fp:
			self.finished_topic = pickle.load(fp)

def main():
	sd = SpiderData()
	sd.spider()

if __name__ == '__main__':
	main()
