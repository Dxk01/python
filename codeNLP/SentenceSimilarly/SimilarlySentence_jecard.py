# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-30

# funcation 处理queries 相似度问题 through jecard distance

import sys
sys.path.append("../..")
sys.path.append("/Users/orion/PycharmProjects/Chat/chat_system/chatter.v2/")
reload(sys)
from chatter.Engine.Ranker.Ranker import Ranker
from DocSimilarlyScriptFile import TextScriptItem
import jieba
import codecs
import logging
from MyCode.tools.WriteResult import WriteResult
from MyCode import config
from MyCode.tools import ReadFile
from chatter.NLP.Semantics.Cilin import Cilin

logging.basicConfig(filename='logger.log',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class SimilarJecard(object):
	def __init__(self):
		logging.info("init class SimilarJecard ")
		cilin = Cilin()
		idfFromQueries = '/Users/orion/PycharmProjects/Chat/chat_system/chatter.v2/Data/Common/Emotion/User/idf.dat'
		self.ranker = Ranker(idfFromQueries)
		self.ranker.setCilin(cilin)
		logging.info("finished init Ranker")
		self.queries = None
		self.queriesRe = None

		return

	#加载数据
	def load(self,file,withId=True,withLabel=True):
		self.queries = dict()
		self.queriesRe = dict()
		self.queryIds = []
		logging.info("load sentences in System")
		with codecs.open(file,'r',encoding="utf-8") as fp:
			for line in fp:
				line = line.strip()

				if len(line) == 0:
					continue

				if line[0] == '$' or line[0] == '#':
					continue

				sid = ''
				label = ''
				text = ''

				tokens = line.split('\t')
				numOfTokens = len(tokens)
				if numOfTokens == 1:
					text = tokens[0]
				elif numOfTokens == 2:
					if withId:
						sid = tokens[0]
						text = tokens[1]
					else:
						text = tokens[0]
				elif numOfTokens == 3:
					if withId:
						sid = tokens[0]
						text = tokens[1]
					else:
						text = tokens[0]

					if withLabel:
						label = tokens[2]
				else:
					logging.error('unexpected line.')
					return

				text_item = TextScriptItem()
				text_item.id = sid
				text_item.text = text
				words = jieba.cut(text.strip().replace(" ",""))
				for w in words:
					text_item.words.append(w)

				self.queryIds.append(sid)
				self.queriesRe[sid] = text_item.words
				self.queries[text] = text_item
			logging.info("finished load sentences in System")

	# 寻找语句的同义句
	def findSimilarSentence(self,userQueryWordList):

		queryById = self.queriesRe
		id_list, max_Simi = self.ranker.findSimilarQueryByIdf(self.queryIds,userQueryWordList,queryById)

		result_sen = []
		for id in id_list:
			result_sen.append(self.queriesRe[id])
		return result_sen

	# 批量处理
	def findSimilarSentences(self, sentences):
		logging.info("find sentence similarly sentence")
		result = {}
		count = 0
		for sen in sentences:
			words = []
			word_list = jieba.cut(sen)

			for w in word_list:
				words.append(w)

			result[sen] = self.findSimilarSentence(words)

			if count % 10 == 0:
				print "finished {0} record".format(count)
			count += 1
		return result


def MyTest():
	print "1"
	filename = config.SimilarlySentencePath + "AllQueriesWithID.txt"
	sentences = ReadFile.readTXTFile(filename)

	# sentences = ReadFile.readTXTFile(config.SimilarlySentencePath + "AllQueriesWithID.txt")
	# test_sentences_doc = ReadFile.readTXTFile(config.SimilarlySentencePath + "corpus_0829.txt")
	test_sentences = []
	# for sen in test_sentences_doc:
	# 	sen_iterms = sen.strip().split("\t")
	# 	if len(sen_iterms) >= 2:
	# 		test_sentences.append(sen_iterms[1])
	train_sentences = []
	for sen in sentences:
		sen_iterms = sen.split("\t")
		# print sen_iterms[1]
		if len(sen_iterms) >= 2:
			# print sen_iterms[1].strip().replace(" ","")
			train_sentences.append(sen_iterms[1].strip().replace(" ", ""))
	print type(train_sentences[0])
	test_sentences = train_sentences

	tsf = SimilarJecard()
	tsf.load(config.SimilarlySentencePath+"AllQueriesWithID.txt")
	result= tsf.findSimilarSentences(test_sentences[:100])

	logging.info("write result to file")
	wr = WriteResult()
	wr.WriteSimilarlySentence(result,file=config.SimilarlySentencePath+"rank_simi_jecard_itfdf.txt")

def main():
	MyTest()

if __name__ == "__main__":
	main()



