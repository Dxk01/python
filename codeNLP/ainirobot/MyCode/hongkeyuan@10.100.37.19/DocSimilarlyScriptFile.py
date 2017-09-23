# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-04

import sys
sys.path.append("../..")
reload(sys)

import logging
import codecs
import jieba

from MyCode import config
from MyCode.tools import ReadFile
from MyCode.tools.WriteResult import WriteResult

class TextScriptItem:
    def __init__(self):
        self.id = ''
        self.text = ''
        self.words = list()

        return

class Ranker(object):
	def __init__(self):
		self.queries = None
		self.queriesRe = None

		return

	def load(self,file,withId=True,withLabel=True):
		self.queries = dict()
		self.queriesRe = dict()

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
				text_item.words.extend(list(jieba.cut(text.strip().replace(" ",""))))

				self.queriesRe[sid] = text_item
				self.queries[text] = text_item


	def getQueryByIndex(self,queryId):
		query = None
		if (self.queriesRe.has_key(queryId)):
			query = self.queriesRe[queryId]
		return query

	def getQueryIndex(self,query):
		"""If the input query exists, return the index, otherwise, return -1"""
		queryId = None
		# inputQuery = self.queriesReverted[2]
		if (self.queries.has_key(query)):
			queryId = self.queries[query].id
		return queryId

	def findSimilarQuery(self, query_words,topn=15):
		candidates = {}
		query_words_list = []
		for w in query_words:
			query_words_list.append(w)
		for query in self.queries:
			query_item = self.queries[query].words
			# print query_item
			sim =  self.calcSimilarityScoreByWordList(query_item,query_words_list)
			if sim == 0.0:
				continue
			candidates[query] = sim

		result = sorted(candidates.iteritems(),key=lambda X:X[1],reverse=True)[:topn]
		return result

	def calcSimilarityScoreByWordList(self, list1, list2):
		"""Calculate similarity score by aligment"""
		score = 0
		set1 = set(list1)
		set2 = set(list2)
		listUnion = set1 | set2
		listjoin = set1 & set2
		return float(len(listjoin))/float(len(listUnion))

	def getSimilarSentences(self,sentences):
		result = {}
		for sen in sentences:
			result[sen] = self.findSimilarQuery(jieba.cut(sen))
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

	tsf = Ranker()
	tsf.load(config.SimilarlySentencePath+"AllQueriesWithID.txt")
	result= tsf.getSimilarSentences(test_sentences)

	wr = WriteResult()
	wr.WriteSimilarSentence(result,file=config.SimilarlySentencePath+"rank_simi.txt")


	# tsf.load(config.SimilarlySentencePath+"AllQueriesWithID.txt",True,True)
	# query_id = tsf.findSimilarQuery(list(jieba.cut("周涛知道是谁么")))
	# print tsf.getQueryByIndex(query_id)

def main():
	MyTest()

if __name__ == "__main__":
	main()