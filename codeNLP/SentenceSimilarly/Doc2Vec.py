# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-30

# funcation 处理queries 相似度问题 文档向量（在此表示句子向量）
import sys
sys.path.append("../..")
reload(sys)
import jieba
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from LabelSentences import LabelSentences
from MyCode import config
from MyCode.tools import ReadFile
from MyCode.tools.WriteResult import WriteResult
import pickle

class  Doc2VecObj(object):
	def __init__(self):
		self.model = None
		self.word_dic = None

	def setcorpus(self,sentences):
		self.sentences = sentences

	def buildModel(self,docs,type_t = 1):
		if type_t == 1:
			# PV-DM w/concatenation - window=5 (both sides) approximates paper's 10-word total window size

			self.model = Doc2Vec(docs,dm=1, dm_concat=1, size=100, window=2, hs=1, min_count=2,workers=2)
		elif type_t == 2:
			# PV-DBOW
			Doc2Vec(docs,dm=0, size=100, hs=0, min_count=2,workers=2)
		elif type_t == 3:
			# PV-DM w/average
			Doc2Vec(docs,dm=1, dm_mean=1, size=100, window=2, hs=0, min_count=2,workers=2)
		# self.model.build_vocab(docs)
		# self.model.train(docs)
		# print('model build success', self.model.vector_size)

	def getCorpus(self,raw_documents):
		corpora_documents = []
		for i, item_text in enumerate(raw_documents):
			words_list = jieba.cut(item_text)
			document = TaggedDocument(words_list=words_list, tags=[i])
			corpora_documents.append(document)
		return corpora_documents

	def calSimilarly(self,sentence):
		test_cut_raw_1 = list(jieba.cut(sentence))
		inferred_vector = self.model.infer_vector(test_cut_raw_1)
		sims = self.model.docvecs.most_similar([inferred_vector])
		return sims

	def calSentencesSimilarly(self,sentences,train_sentences):
		result = {}
		for sen in sentences:
			if sen in result:
				continue
			indexs = self.calSimilarly(sentence=sen)
			if indexs == None:
				continue
			values = []
			for index in indexs:
				# if index[1] > 0.5:
				values.append(train_sentences[index[0]])
			result[sen] = values
		return result

	def save(self,model_name = "doc2vec_1"):
		file = config.ModelPath + model_name +".model"
		with open(file,"wb") as fp:
			pickle.dump(self.model,fp)

	def load(self,model_name="doc2vec_1"):
		file = config.ModelPath + model_name + ".model"
		try :
			with open(file, "rb") as fp:
				self.model = pickle.load(fp)
		except:
			self.model = None

	# 计算 句子的距离  值越大说明差别越大，越不相似
	def similarly(self, sent1, sent2):
		# sentence_1 = self.similar.index(sent1)
		# sentence_2 = self.similar.index(sent2)
		return self.model.wmdistance(sent1,sent2)

	def similarlySentences(self,sentences):

		for sen in sentences:

			for sen1 in sentences:
				print "{0} <-----> {1} 的相似度是：{2}".format(sen,sen1,self.similarly(sen,sen1))
			print

	# 计算句子最相似的topn 哥个句子，返回句子和相似度
	def most_similarSentence(self,sentence,sentences,topn=1):
		topnSentence = {}
		count = 0
		for sent in sentences:
			topnSentence[sent] = self.similarly(sentence,sent)
			count += 1
		return sorted(topnSentence.iteritems(),key=lambda X:X[1],reverse=False)[:topn]






def main():
	# train_sentences = [
	# 	'0无偿居间介绍买卖毒品的行为应如何定性',
	# 	'1吸毒男动态持有大量毒品的行为该如何认定',
	# 	'2如何区分是非法种植毒品原植物罪还是非法制造毒品罪',
	# 	'3为毒贩贩卖毒品提供帮助构成贩卖毒品罪',
	# 	'4将自己吸食的毒品原价转让给朋友吸食的行为该如何认定',
	# 	'5为获报酬帮人购买毒品的行为该如何认定',
	# 	'6毒贩出狱后再次够买毒品途中被抓的行为认定',
	# 	'7虚夸毒品功效劝人吸食毒品的行为该如何认定',
	# 	'8妻子下落不明丈夫又与他人登记结婚是否为无效婚姻',
	# 	'9一方未签字办理的结婚登记是否有效',
	# 	'10夫妻双方1990年按农村习俗举办婚礼没有结婚证 一方可否起诉离婚',
	# 	'11结婚前对方父母出资购买的住房写我们二人的名字有效吗',
	# 	'12身份证被别人冒用无法登记结婚怎么办？',
	# 	'13同居后又与他人登记结婚是否构成重婚罪',
	# 	'14未办登记只举办结婚仪式可起诉离婚吗',
	# 	'15同居多年未办理结婚登记，是否可以向法院起诉要求离婚'
	# ]
	filename = config.SimilarlySentencePath+"AllQueriesWithID.txt"
	sentences = ReadFile.readTXTFile(filename)

	# sentences = ReadFile.readTXTFile(config.SimilarlySentencePath + "AllQueriesWithID.txt")
	test_sentences_doc = ReadFile.readTXTFile(config.SimilarlySentencePath + "corpus_0829.txt")
	test_sentences = []
	for sen in test_sentences_doc:
		sen_iterms = sen.strip().split("\t")
		if len(sen_iterms) >= 2:
			test_sentences.append(sen_iterms[1])
	train_sentences = []
	for sen in sentences:
		sen_iterms = sen.split("\t")
		# print sen_iterms[1]
		if len(sen_iterms) >= 2:
			# print sen_iterms[1].strip().replace(" ","")
			train_sentences.append(sen_iterms[1].strip().replace(" ", ""))
	print type(train_sentences[0])
	docs = LabelSentences(filename=None,sentences=train_sentences)
	# docs = LabelSentences.LabelSentences(sentences=train_sentences)

	# sentences = ReadFile.readTXTFile(config.SimilarlySentencePath+"corpus_0829.txt")

	# train_sentences = ReadFile.getFileSentence(config.SimilarlySentencePath + "")
	# print len(sentences)
	# train_sentences = []
	# for sen in sentences:
	# 	sen_iterms = sen.split("\t")
	# 	if len(sen_iterms) == 2:
	# 		print sen_iterms[1]
	# 		train_sentences.append(sen_iterms[1])
	# test_sentences = ReadFile.readTXTFile(config.SimilarlySentencePath+"corpus_0829_t.txt")
	# test_sentences = ['周涛知道是谁吗']
	test_sentences = train_sentences[:100]
	SSO = Doc2VecObj()
	# corpus = SSO.getCorpus(docs)
	# SSO.buildModel(docs)
	# SSO.save()

	print " load model"
	SSO.load()
	value = SSO.similarly(u"早起吃的油条，很好吃。",u"今天吃什么")
	# result = SSO.most_similarSentence(test_sentences[9],test_sentences[:200],topn=10)
	# print test_sentences[9]
	# for re in result:
	# 	print re[0],re[1]
	print "similarly : ", value
	# result = SSO.most_similarSentence(test_sentences,train_sentences)
	# Wr = WriteResult()
	# can_not_deal = Wr.WriteSimilarlySentence(result,"Doc2Vec_simi.txt")

if __name__ == '__main__':
	main()
