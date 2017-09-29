# encoding: utf-8
"""
作者：liguoyu
"""
import time
from MyCode import config
import random
from SpiderTopicQuestions import SpiderTopicQuestions
from TopicTree import TopicTree


class SpiderData(object):
	""" 批量爬取 多个话题的 批量的问题数据 并标记 问题的话题ID """
	def __init__(self, spider_number=2000, savefile=config.TopicFilePath+"topic_questions.csv"):
		topictree = TopicTree()
		topictree.paserData(data=topictree.load(config.TopicFilePath+'zhihu_topic_link_1.json'))

		self.topics = topictree.getDeepTopic()

		self.spider_topic_questions = SpiderTopicQuestions()
		self.spider_topic_questions.setQuestions_number(spider_number)
		self.spider_topic_questions.setSaveFile(file=savefile)

	def spider(self):
		for topic in self.topics:
			self.spider_topic_questions.Spider(topic)
			time.sleep(random.randint(4,10))

def main():
	sd = SpiderData()
	sd.spider()

if __name__ == '__main__':
	main()
