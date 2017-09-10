# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-30

# funcation 处理queries 相似度问题
import sys
sys.path.append("../..")
reload(sys)
from gensim import corpora
from gensim.similarities.docsim import Similarity
import jieba
from MyCode.tools import ReadFile
from MyCode import config
import pickle
from MyCode.tools.WriteResult import WriteResult

class SentenceSimilarlyObj(object):

	def __init__(self):
		# self.model = None
		self.corpus = None
		self.word_dic = None
		self.similar = None
		self.num_feature = 0

	def getCorpus(self,raw_documents):
		corpora_documents = []
		for item_text in raw_documents:
			item_str = list(jieba.cut(item_text))
			corpora_documents.append(item_str)
		# 生成字典和向量语料
		self.word_dic = corpora.Dictionary(corpora_documents)
		# self.word_dic = LDA_Topic.load_word_dic()
		self.num_feature = len(self.word_dic)
		print "特征数量：{0}".format(self.num_feature)
		corpus = [self.word_dic.doc2bow(text) for text in corpora_documents]
		return corpus

	def setSimilar(self,simi_name = config.SimilarlySentencePath+"simi_index/Similarity-index",corpus=None):
		self.similar = Similarity(simi_name,corpus,self.num_feature)

	def calSentenceSimilarly(self,sentence,num_best=15):
		# print type(sentence)
		print sentence
		test_cut_raw_1 = list(jieba.cut(sentence))
		# print test_cut_raw_1
		test_corpus_1 = self.word_dic.doc2bow(test_cut_raw_1)
		self.similar.num_best = num_best
		# print test_corpus_1
		try:
			# print test_corpus_1
			result = self.similar[test_corpus_1]
			return result
		except:
			print "error"
			return []

	def calSentencesSimilarly(self,sentences,train_sentences):
		result = {}
		# can_result = []
		for sen in sentences:
			if sen in result:
				continue
			indexs = self.calSentenceSimilarly(sentence=sen)
			# print indexs
			if indexs == None:
				continue
			values = []
			# if len(values) <2:
				# can_result =
			for index in indexs:
				if index[1] > 0.5:
					values.append(train_sentences[index[0]])

			result[sen] = values
		return result

	def save(self,model_name = "simi_sentence_2",word_dic = "simi_word_dic_2"):
		file = config.ModelPath + model_name +".model"
		word_dic_file = config.ModelPath + word_dic +".model"
		with open(file,"wb") as fp:
			pickle.dump(self.similar,fp)
		with open(word_dic_file,"wb") as wordfp:
			pickle.dump(self.word_dic,wordfp)

	def load(self,model_name="simi_sentence_2",word_dic = "simi_word_dic_2"):
		file = config.ModelPath + model_name + ".model"
		word_dic_file = config.ModelPath + word_dic + ".model"
		try :
			with open(file, "rb") as fp:
				self.similar = pickle.load(fp)
			with open(word_dic_file, "rb") as wordfp:
				self.word_dic = pickle.load(wordfp)
		except:
			self.word_dic = None
			self.similar = None

	def similarly(self, sent1, sent2):
		# sentence_1 = self.similar.index(sent1)
		# sentence_2 = self.similar.index(sent2)
		print self.similar.wmdistance(sent1,sent2)

def findCan_not_deal_data(test_sentences,can_not_deal_data):
	result = []
	for sen in test_sentences:
		print sen
		sen_iterms = sen.strip().split("\t")
		if len(sen_iterms) >= 2:
			print sen_iterms[1]
			if sen_iterms[1] in can_not_deal_data:
				result.append(sen)
	
	return result
			

def main():
	sentences = ReadFile.readTXTFile(config.SimilarlySentencePath + "AllQueriesWithID.txt")
	test_sentences_doc = ReadFile.readTXTFile(config.SimilarlySentencePath + "corpus_0829.txt")
	test_sentences = []
	for sen in test_sentences_doc:
		sen_iterms = sen.strip().split("\t")
		if len(sen_iterms) >= 2:
			test_sentences.append(sen_iterms[1])

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
	# print type(train_sentences[0])
	# print len(sentences)
	train_sentences = []
	for sen in sentences:
		sen_iterms = sen.split("\t")
		# print sen_iterms[1]
		if len(sen_iterms) >= 2:
			# print sen_iterms[1].strip().replace(" ","")
			train_sentences.append(sen_iterms[1].strip().replace(" ",""))
	print type(train_sentences[0])
	#
	# print "build simi_model"
	SSO = SentenceSimilarlyObj()

	corpus = SSO.getCorpus(train_sentences)
	SSO.setSimilar(corpus=corpus)
	print "save simi model"
	SSO.save()
	SSO.save("simi_model_little","word_dic_little")
	print "build success"

	# print "load model"
	# SSO.load()
	# print SSO.similar

	print "test"
	# indexs = SSO.calSentenceSimilarly(sentence=u"说说后天是礼拜几")
	# for index in indexs:
	# 	print index[0],train_sentences[index[0]],index[1]
	# sent1 = corpus[0]
	# sent2 = corpus[1]
	# SSO.similarly(sent1, sent2)
	result = SSO.calSentencesSimilarly(train_sentences[:100],train_sentences)
	Wr = WriteResult()
	can_not_deal = Wr.WriteSimilarlySentence(result,config.SimilarlySentencePath+"docSim_simi.txt")
	# final_re = findCan_not_deal_data(test_sentences,can_not_deal)
	# Wr.WriteCanNot_deal_Sentence(final_re)
	# for i in xrange(2,100):
	# 	for sen in train_sentences:
		# try:
		# 	sentences_indexs = SSO.calSentenceSimilarly(sentence=train_sentences[i])
		# 	print "1"
		# 	print sentences_indexs
		# 	print index
		# 	for index in sentences_indexs:
		# 		print train_sentences[index[0]].strip()
		# 	print "2"
		# except Exception,e:
		# 	continue


if __name__ == '__main__':
    main()


		
