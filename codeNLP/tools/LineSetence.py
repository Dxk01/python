# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-07

# funcation 处理 句子文本分词迭代器

import  jieba

class LineSentence(object):
	def __init__(self,sentences):
		self.sentences = sentences

	def __iter__(self):
		for sen in self.sentences:
			yield list(jieba.cut(sen.strip().replace(" ","")))
