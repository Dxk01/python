# -*- coding:utf8 -*-
"""
作者：liguoyu
"""

# import sys
# sys.setdefaultencoding('utf8')
# reload(sys)
import time
from Login import Login
import urllib2
import random
import re
import os
from MyCode import config
import codecs



class SpiderTopicQuestions(object):
	"""
	爬取知乎某一话题下的数据
	"""
	def __init__(self):
		"""
		初始化相关参数
		"""
		self.getQuestions_number = 2000
		self.savefilename = None

	def setSaveFile(self,file=config.TopicFilePath+"topic_questions.csv"):
		self.savefilename = file

	def setQuestions_number(self,number=2000):
		self.getQuestions_number = number

	def getOnePageContent(self,url='https://www.zhihu.com/topic/19661050/questions?page=2'):
		"""
		获取网页内容
		:param url:
		:return:
		"""
		# 构建请求的 request
		request = urllib2.Request(url)
		# 获取请求的页面 HTML 代码
		response = urllib2.urlopen(request)
		# 将页面代码转成 UTF-8
		pageCode = response.read().decode('utf-8')
		return pageCode

	def paserContent(self,text):
		"""
		解析 html text 内容提取问题 ID 和 问题文本
		:param text:
		:return:
		"""
		pattern = re.compile(r'href="/question/(.*?)">(.*?)</a>', re.S)
		items = re.findall(pattern, text)
		questions = []
		for item in items:
			if '40470324' in item[0]:
				continue
			question_id = item[0]
			sub_items = item[1].split(">")
			length = len(sub_items)-1
			question_text = sub_items[length]
			questions.append([question_id,question_text.encode('utf8')])
		return questions

	def getTopicQuestions(self,topic_id='19661050'):
		base_url = 'https://www.zhihu.com/topic/{}/questions'.format(topic_id)
		print base_url
		state = True
		i = 1
		questions = []
		while state:
			url = base_url + "?page={}".format(i)
			print url
			i += 1
			text = self.getOnePageContent(url)
			page_questions = self.paserContent(text)
			if not page_questions:
				state = False
			questions.extend(page_questions)
			if len(questions) > self.getQuestions_number:
				break
			time.sleep(random.randint(1,5))

		for question in questions:
			question.append(topic_id)
		return questions

	def show(self,questions):
		for q in questions:
			print "question ID: {} \t question: {}\t topic: {}".format(q[0],q[1],q[2])

	def writeResultToFile(self,questions):
		if not os.path.exists(self.savefilename):
			with codecs.open(self.savefilename,'a',encoding='utf8') as fp:
				fp.write(u'ID\tQuestion\ttopicID\n')

		with codecs.open(self.savefilename,'a',encoding='utf8') as fp:
			for q in questions:
				# print q[0],q[1],q[2]
				fp.write(u"{}\t{}\t{}\n".format(q[0],unicode(q[1], "utf8"),q[2]))

	def Spider(self,topic_id):
		questions = self.getTopicQuestions(topic_id)
		self.writeResultToFile(questions)
		print "cur topic {} finished spider !\nspider data {}".format(topic_id,len(questions))



def main():
	stq = SpiderTopicQuestions()
	stq.setSaveFile()
	questions = stq.getTopicQuestions()
	stq.show(questions)
	stq.writeResultToFile(questions)

if __name__ == '__main__':
	main()


