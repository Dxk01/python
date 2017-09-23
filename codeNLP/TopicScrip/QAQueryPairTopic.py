# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-11

from MyCode.Algorithm.HDA import HDA
from MyCode.tools import ReadFile
from MyCode import config
from MyCode.tools.WriteResult import WriteResult

class QAQueryPairTopic(object):
	def __init__(self):
		Lda_topic = HDA("test_Hda", "test_Hda_word")
		Lda_topic.load_word_dic()
		Lda_topic.load_HDAModel()
		self.model = Lda_topic

	def getQAQueryTopicId(self,sentence):
		iterms = sentence.strip().split("\t")
		if len(iterms) != 2:
			return None
		Q_topic = self.model.getTopicLab(iterms[0])
		R_topic = self.model.getTopicLab(iterms[1])
		if Q_topic[1] >= 0.8:
			return (Q_topic[0],R_topic[0])
		else:
			return None

	def getgetQAQueriesTopicId(self,sentences):
		result = []
		topics = []
		for sen in sentences:
			re = self.getQAQueryTopicId(sen)
			if re:
				result.append(re)
				topics.append(re[0])
				topics.append(re[1])
		return result,list(set(topics))

	def getResponseTopicId(self,sentence):
		re = self.model.getTopicLab(sentence)
		if re[1] >= 0.7:
			return re[0]
		else:
			return None

	def getResponsesTopic(self,sentences):
		result = []
		for sen in sentences:
			iterms = sen.strip().split("\t")
			if len(iterms) < 2:
				continue
			else:
				re = self.getResponseTopicId(iterms[1])
				if re:
					result.append((re,iterms[1]))
		return result

def main():
	sentences = ReadFile.readTXTFile(config.TopicFilePath+"QRpair.txt")
	qaQueryPairTopic = QAQueryPairTopic()
	result = qaQueryPairTopic.getgetQAQueriesTopicId(sentences)
	wr = WriteResult()
	wr.WriteTopicRegular(result[0])
	wr.WriteTopic(result[1])
	result = qaQueryPairTopic.getResponsesTopic(sentences)
	wr.WriteResponseWithTopicId(result)

if __name__ == "__main__":
	main()