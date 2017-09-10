# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-01

# class for dealing sentence lab preprocess for doc2vec
import codecs
from gensim.models.doc2vec import TaggedDocument
import jieba

class LabelSentences(object):
	def __init__(self,filename=None,sentences=None):
		self.filename = filename
		self.sentences = sentences

	# read data from file
	def __iter__(self):
		if self.filename:
			with codecs.open(self.filename,"r",encoding="utf8") as fp:
				for index,line in enumerate(fp):
					yield TaggedDocument(list(jieba.cut(line.strip().replace(" ",""))),tags=[index])
		if self.sentences:
			for index,line in enumerate(self.sentences):
				yield TaggedDocument(list(jieba.cut(line.strip().replace(" ",""))), tags = [index])

	# def __iter__(self,sentences):
	# 	for index,line in enumerate(sentences):
	# 		yield TaggedDocument(list(jieba.cut(line.strip())), tags = index)




