# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-30

from MyCode import config
from MyCode.tools.ReadFile import getQueriesSentence
from MyCode.tools.LineSetence import LineSentence
import math
import codecs

class biterm(object):
	def __int__(self,w1,w2):
		self.W1 = w1
		self.W2 = w2
		self.Z = 0  # topic assignment

	def __cmp__(self, other):
		if (self.W1 == other.W1 and self.W2 == other.W2) or \
			(self.W1 == other.W2 and self.W2 == other.W1):
			return True
		return False



	def count(self):
		self.frequently += 1

	def setCount(self,count=0):
		self.frequently = count


class BurstyBTM(object):
	"""
		class define Biterm topic model based paper follow
		* Bursty Biterm topic model(BTM) with Gbbis sampling implementation
        * Author: Xiaohui Yan(xhcloud@gmail.com)
		* Paper:
		*     `Xiaohui Yan, et al. A Probabilistic Model for Bursty Topic Discovery in Microblogs. AAAI 2015.`
        * 2014-6-25
	"""

	def __int__(self, type, topic_num=20, vocab_size=None, alpha=1.0, beta=0.1, iter_num=100):
		"""
			初始化 模型 超参数
		:param type : 's' is simplified, 'n' is normal
		:param topic_num: topic number 话题数
		:param vocab_size: word dictionary size 词典大小
		:param alpha: alpha 参数，话题分布的超参数
		:param beta: beta 参数，词 话题分布 超参数
		:param iter_num: 迭代次数
		:return:
		Notice : topic_num 是 话题数目，对象的总话题数是 topic_num + 1 所以这里存在一个背景话题
		"""
		self.type = type
		self.topic_num = topic_num
		self.vocab_size = vocab_size

		self.alpha = alpha
		self.beta = beta

		self.iter_num = iter_num

		self.nb_z = None       # number of biterms assigned to topic z, size (topic_num + 1) * 1
		self.nb = None         # number of biterms assigned to bursty topics
		self.nwz = None        # times of w in bustry topic z ,size (topic_num + 1) * W
		self.bs = None
		self.etas = None

	def loadData(self,file='btm_text_corpus.txt'):
		sentences = []
		with codecs.open(file, 'r', encoding='utf8') as fp:
			[sentences.append(line.strip().split(' ')) for line in fp]

		return sentences

	def build_word_dic(self,sentences):
		"""
			构建词典,并统计 各词的词频（整个语料中）
		:param sentences:
		:return:
		"""
		self.word_dic = {}   # 词典 索引
		self.word_fre = {}   # word frequently
		word_id = 1
		for sentence in sentences:
			for word in sentence:
				if word not in self.word_dic:
					self.word_dic[word] = word_id
					word_id += 1

				word_index = self.word_dic[word]
				if word_index in self.word_fre:
					self.word_fre[word_index] += 1
				else:
					self.word_fre[word_index] = 1
		self.vocab_size = len(self.word_dic.keys())

	def build_wordId(self,sentences):
		"""
		将文本 中word 映射到 word_id 并将结果存储到文件
		:param sentences: 切词后的文档
		:return: 当回 文档的 [wid,...,wid]列表
		"""
		with codecs.open("word_id.txt",'w',encoding='utf8') as fp:
			for sentence in sentences:
				doc = []
				# print sentence
				for word in sentence:
					doc.append(self.word_dic[word])
				wid_list = [str(wid) for wid in doc]
				# print wid_list
				fp.write(' '.join(wid_list)+"\n")

	def build_Biterms(self,sentence):
		"""
		获取 document 的 biterms
		:param sentence:
		:return: biterm list
		"""
		win = 15 # 设置窗口大小
		biterms = []
		for i in xrange(len(sentence)-1):
			for j in xrange(i+1, min(i+win+1, len(sentence))):
				wi = int(sentence[i])
				wj = int(sentence[j])
				if wi > wj:
					tem = wi
					wi = wj
					wj = tem
				biterms.append([wi,wj])
		return biterms

	def loadwordId(self,file='word_id.txt'):
		"""
		获取语料的词 ID
		:param file:
		:return:
		"""
		sentences_wordId = []
		with open(file, 'r') as fp:
			[sentences_wordId.append(line.strip().split(" ")) for line in fp]
		return sentences_wordId

	def staticBitermFrequence(self,sentences):
		"""
		统计 biterms 的频率
		:param sentences: 使用word id 表示的 sentence 列表
		:return: 返回corpus 中各个 biterm （wid,wid）: frequence 的频率
		"""
		self.biterms = {}
		for sentence in sentences:
			bits = self.build_Biterms(sentence)
			for bit in bits:
				key = str(bit[0]) + " "+ str(bit[1])
				if key in self.biterms:
					self.biterms[key] += 1
				else:
					self.biterms[key] = 1

		with open("biterm_freq.txt", 'w') as fp:
			for key in self.biterms:
				fp.write(key+"\t"+str(self.biterms[key])+"\n")

	def loadBitermFrequence(self,file="biterm_freq.txt"):
		self.etas = {}
		with open(file, "r") as fp:
			for line in fp:
				b,f = line.strip().split("\t")
				f = float(f)
				self.etas[b] = self.computeEta(f)

	def computeEta(self,f):
		"""
		计算 eta
		:param f:
		:return:
		"""
		eps = 0.01      # epsilon in the paper
		# avgf = sum(df.values()) / float(len(df))
		pass

def main():
	bBtm = BurstyBTM()
	sentences = bBtm.loadData()
	bBtm.build_word_dic(sentences)
	sentences_wordId = bBtm.loadwordId()
	bBtm.staticBitermFrequence(sentences_wordId)
	# bBtm.build_wordId(sentences)
	# for sen in sentences:
	# 	print sen

if __name__ == '__main__':
	main()