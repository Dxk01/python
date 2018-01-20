# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-10-10
import sys

sys.path.append("/Users/orion/PycharmProjects/Test2/MyCode")
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import codecs
import random
from Biterm import Biterm
import pickle
from MyCode import config
from MyCode.tools.filterStopWords import filterStopWords
import jieba
import time
from MyCode.tools.ReadFile import readTXTFile
import cPickle
from sklearn.cluster import k_means
from sklearn.naive_bayes import MultinomialNB
# from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
# from sklearn.neighbors import
from sklearn.neural_network import MLPClassifier
from sklearn import metrics


# from MyCode.Algorithm.tfMultyPerceptron import tfMultyPerceptron
# from MyCode.Algorithm.FNN import Net


def buildTestFile(file=config.BTMData + "topic_questions_2.csv"):
	train_data = []
	topics = []
	with open(config.BTMData + "sentence_and_topic.txt", 'r') as fp:
		for line in fp:
			term = line.strip().split("\t")
			train_data.append(term[0])
			topics.append(term[1])
	topics = list(set(topics))
	test_data = []
	with open(file, 'r') as fp:
		for line in fp:
			term = line.strip().split("\t")
			# print term
			if len(term) != 3:
				continue
			if term[2] in topics and term[1] not in train_data:
				test_data.append(term[1:])

	with open(config.BTMData + "test.txt", "w") as fp:
		for sentence in test_data:
			fp.write("\t".join(sentence) + "\n")


class BtmModel(object):
	"""
		biterm Topic Model
	"""

	def __init__(self, topic_num, iter_times, alpha, beta, has_background=False):
		"""
			初始化 模型对象
		:param voca_size: 词典大小
		:param topic_num: 话题数目
		:param iter_times: 迭代次数
		:param save_step:
		:param alpha: hyperparameters of p(z)
		:param beta:  hyperparameters of p(w|z)
		"""
		self.biterms = list()
		self.voca_size = 0
		self.real_topic_num = topic_num
		self.topic_num = self.real_topic_num
		self.n_iter = iter_times

		self.alpha = alpha
		self.beta = beta

		self.nb_z = list()  # int 类型，n(b|z) ,size topic_num+1
		self.nwz = None  # int 类型矩阵， n(w,z), size topic_num * voca_size
		self.pw_b = list()  # double 词的统计概率分布
		self.has_background = has_background

	def preProcess(self, file=config.BTMData + 'btm_text_corpus.txt'):
		"""
		过滤 停用词
		:param file:
		:return:
		"""
		sentences = []
		with codecs.open(file, 'r', encoding='utf8') as fp:
			for sen in fp:
				term = sen.strip().split(' ')
				result = filterStopWords(term)
				sentences.append(result)
		with codecs.open(config.BTMData + "filterStopWord.txt", 'w', encoding='utf8') as fp:
			[fp.write(" ".join(line) + '\n') for line in sentences if line]

	def loadData(self, file=config.BTMData + 'filterStopWord.txt'):
		"""
		加载文本数据，文本是已经经过分析处理
		（最好经过词过滤 去除文本中的 停用词，无意义词等）
		:param file: 文件路径
		:return:
		"""
		sentences = []
		size = 1000000
		with codecs.open(file, 'r', encoding='utf8') as fp:
			[sentences.append(line.strip().split(' ')) for line in fp if len(sentences) <= size]

		return sentences

	def build_word_dic(self, sentences):
		"""
			构建词典,并统计 各词的词频（整个语料中）
		:param sentences:
		:return:
		"""
		self.word_dic = {}  # 词典 索引
		self.word_fre = {}  # word frequently
		word_id = 1
		for sentence in sentences:

			for word in sentence:
				if word not in self.word_dic:
					self.word_dic[word] = word_id
					word_id += 1
					self.voca_size += 1

				word_index = self.word_dic[word]
				if word_index in self.word_fre:
					self.word_fre[word_index] += 1
				else:
					self.word_fre[word_index] = 1
		self.voca_size = len(self.word_fre.keys())
		sum_val = sum(self.word_fre.values())
		smooth_val = 0.001
		# 归一化，正则化
		for key in self.word_fre:
			self.word_fre[key] = (self.word_fre[key] + smooth_val) / (sum_val + smooth_val * (self.topic_num + 1))
		with codecs.open(config.BTMData + "PreProcess/word_freq.txt", 'w', encoding='utf8') as fp:
			for key in self.word_fre:
				fp.write("{}\t{}\n".format(key, self.word_fre[key]))
		with open(config.BTMData + "PreProcess/word_dic.txt", 'w') as fp:
			for key in self.word_dic:
				# print "{}\t{}".format(str(key), self.word_dic[key])
				fp.write(str(key) + "\t" + str(self.word_dic[key]) + "\n")

	def build_wordId(self, sentences):
		"""
		将文本 中word 映射到 word_id 并将结果存储到文件
		:param sentences: 切词后的文档
		:return: 当回 文档的 [wid,...,wid]列表
		"""
		with codecs.open(config.BTMData + "PreProcess/word_id.txt", 'w', encoding='utf8') as fp:
			for sentence in sentences:
				doc = []
				# print sentence
				for word in sentence:
					doc.append(self.word_dic[word])
				wid_list = [str(wid) for wid in doc]
				# print wid_list
				fp.write(' '.join(wid_list) + "\n")

	def build_Biterms(self, sentence):
		"""
		获取 document 的 biterms
		:param sentence: word id list sentence 是切词后的每一词的ID 的列表
		:return: biterm list
		"""
		win = 15  # 设置窗口大小
		biterms = []
		# with codecs.open("word_id.txt", 'r', encoding="utf8") as fp:
		# 	sentence = []
		# sentence =
		if not sentence or len(sentence) <= 1:
			return biterms
		for i in xrange(len(sentence) - 1):
			for j in xrange(i + 1, min(i + win + 1, len(sentence))):
				biterms.append(Biterm(int(sentence[i]), int(sentence[j])))
		return biterms

	def loadwordId(self, file=config.BTMData + 'PreProcess/word_id.txt'):
		"""
		获取语料的词 ID
		:param file:
		:return:
		"""
		sentences_wordId = []
		with open(file, 'r') as fp:
			[sentences_wordId.append(line.strip().split(" ")) for line in fp]
		return sentences_wordId

	def staticBitermFrequence(self):
		"""
		统计 biterms 的频率
		:param sentences: 使用word id 表示的 sentence 列表
		:return: 返回corpus 中各个 biterm （wid,wid）: frequence 的频率
		"""
		sentences = []
		with codecs.open(config.BTMData + "PreProcess/word_id.txt", 'r', encoding="utf8") as fp:
			sentences = [line.strip().split(" ") for line in fp]
		self.biterms = []
		for sentence in sentences:
			bits = self.build_Biterms(sentence)
			self.biterms.extend(bits)
		with open(config.BTMData + "PreProcess/biterm_freq.txt", 'w') as fp:
			for key in self.biterms:
				fp.write(str(key.get_word()) + " " + str(key.get_word(2)) + "\n")

	def model_init(self):
		"""
		模型初始化
		:return:
		"""
		# 初始化 话题 biterm 队列和word -topic 矩阵
		self.nb_z = [0] * (self.topic_num + 1)
		self.nwz = np.zeros((self.topic_num, self.voca_size))

		for bit in self.biterms:
			k = random.randint(0, self.topic_num - 1)
			self.assign_biterm_topic(bit, k)

	def assign_biterm_topic(self, bit, topic_id):
		"""
		为 biterm 赋予 topic ，并更新 相关nwz 及 nb_z 数据
		:param bit:
		:param topic_id:
		:return:
		"""
		w1 = int(bit.get_word()) - 1
		w2 = int(bit.get_word(2)) - 1
		bit.setTopic(topic_id)
		self.nb_z[topic_id] += 1
		self.nwz[int(topic_id)][w1] = self.nwz[int(topic_id)][w1] + 1
		self.nwz[int(topic_id)][w2] = self.nwz[int(topic_id)][w2] + 1

	def Init_MOdel(self, doc_pt=config.BTMData + "btm_text_corpus.txt"):
		"""
		初始化模型
		:return:
		"""
		sentences = self.loadData(doc_pt)
		self.build_word_dic(sentences)
		self.build_wordId(sentences)
		self.staticBitermFrequence()
		self.model_init()

	def CombbineTopic(self):
		# self.real_topic_num = self.topic_num / 3
		array_topic_bit = np.c_[self.nwz, self.nb_z[:-1]]

		self.topic_nwz = k_means(self.nwz, n_clusters=self.real_topic_num)[1]
		print self.topic_nwz

	def runModel(self, res_dir=config.BTMData + "output/"):
		"""
		运行构建模型
		:param doc_pt: 数据源文件路径
		:param res_dir: 结果存储文件路径
		:return:
		"""
		print "Begin iteration"
		out_dir = res_dir + "k" + str(self.topic_num) + '.'
		for iter in xrange(self.n_iter):
			print "\r当前迭代{}，总迭代{}".format(iter, self.n_iter)
			for bit in self.biterms:
				self.updateBiterm(bit)

	def Mul_updateBiterm(self, bit):
		pass

	def updateBiterm(self, bit):
		self.reset_biterm(bit)

		pz = [0] * self.topic_num
		self.compute_pz_b(bit, pz)

		#
		topic_id = self.mult_sample(pz)
		self.assign_biterm_topic(bit, topic_id)

	def compute_pz_b(self, bit, pz):
		"""
		更新 话题的概率分布
		:param bit:
		:param pz:
		:return:
		"""
		w1 = bit.get_word() - 1
		w2 = bit.get_word(2) - 1
		for k in xrange(self.topic_num):
			if self.has_background and k == 0:
				pw1k = self.pw_b[w1]
				pw2k = self.pw_b[w2]
			else:
				pw1k = (self.nwz[k][w1] + self.beta) / (2 * self.nb_z[k] + self.voca_size * self.beta)
				pw2k = (self.nwz[k][w2] + self.beta) / (2 * self.nb_z[k] + 1 + self.voca_size * self.beta)
			pk = (self.nb_z[k] + self.alpha) / (len(self.biterms) + self.topic_num * self.alpha)
			pz[k] = pk * pw1k * pw2k

	def mult_sample(self, pz):
		"""
		sample from mult pz
		:param pz:
		:return:
		"""
		for i in xrange(1, self.topic_num):
			pz[i] += pz[i - 1]

		u = random.random()
		k = None
		for k in xrange(0, self.topic_num):
			if pz[k] >= u * pz[self.topic_num - 1]:
				break
		if k == self.topic_num:
			k -= 1
		return k

	def show(self, top_num=10):
		print "BTM topic model \t",
		print "topic number {}, voca word size : {}".format(self.topic_num, self.voca_size)
		word_id_dic = {}
		for key in self.word_dic:
			word_id_dic[self.word_dic[key]] = key

		for topic in xrange(self.topic_num):
			print "topic id : {}".format(topic),
			print "\ttopic top word \n",
			b = zip(self.nwz[int(topic)], range(self.voca_size))
			b.sort(key=lambda x: x[0], reverse=True)
			for index in xrange(top_num):
				print word_id_dic[b[index][1] + 1], b[index][0],
			print

	def SentenceProcess(self, sentence):
		"""
		文本预处理
		:param sentence: 输入文本
		:return:
		"""
		# 去停用词等过滤处理
		words = filterStopWords(jieba.cut(sentence))
		words_id = []
		# 将文本转换为 word ID
		# print words
		self.count = 0
		for w in words:
			if w in self.word_dic:
				# self.voca_size += 1
				# self.word_dic[w] = self.voca_size
				words_id.append(self.word_dic[w])
		return self.build_Biterms(words_id)

	def sentence_topic(self, sentence, topic_num=1, min_pro=0.01):
		"""
		计算 sentence 最可能的话题属性,基于原始的LDA 方法
		:param sentence: sentence
		:param topic_num: 返回 可能话题数目 最多返回
		:param min_pro: 话题概率最小阈值，只有概率大于该值，才是有效话题，否则不返回
		:return: 返回可能的话题列表，及话题概率
		"""
		words_id = self.SentenceProcess(sentence)
		topic_pro = [0.0] * self.topic_num
		sentence_word_dic = [0] * self.voca_size
		weigth = 1.0 / len(words_id)
		for word_id in words_id:
			sentence_word_dic[word_id] = weigth
		for i in xrange(self.topic_num):
			topic_pro[i] = sum(map(lambda x, y: x * y, self.nwz[i], sentence_word_dic))
		sum_pro = sum(topic_pro)
		topic_pro = map(lambda x: x / sum_pro, topic_pro)
		# print topic_pro
		min_result = zip(topic_pro, range(self.topic_num))
		min_result.sort(key=lambda x: x[0], reverse=True)
		result = []
		for re in min_result:
			if re[0] > min_pro:
				result.append(re)

		return result[:topic_num]

	def infer_sentence_topic(self, sentence, topic_num=1, min_pro=0.001):
		"""
		BTM topic model to infer a document or sentence 's topic
		基于 biterm s 计算问题
		:param sentence: sentence
		:param topic_num: 返回 可能话题数目 最多返回
		:param min_pro: 话题概率最小阈值，只有概率大于该值，才是有效话题，否则不返回
		:return: 返回可能的话题列表，及话题概率
		"""
		sentence_biterms = self.SentenceProcess(sentence)

		topic_pro = [0] * self.topic_num
		# 短文本分析中，p (b|d) = nd_b/doc(nd_b)  doc(nd_b) 表示 计算的query 的所有biterm的计数
		# 因此，在short text 的p(b|d) 计算为1／biterm的数量
		bit_size = len(sentence_biterms)
		if not sentence_biterms:
			return [(1.0, -1)]
		for bit in sentence_biterms:
			# cal p(z|d) = p(z|b)*p(b|d)
			# cal p(z|b)
			pz = [0] * self.topic_num
			self.compute_pz_b(bit, pz)
			pz_sum = sum(pz)
			pz = map(lambda pzk: pzk / pz_sum, pz)

			for x, y in zip(range(self.topic_num), pz):
				topic_pro[x] += y / bit_size

		min_result = zip(topic_pro, range(self.topic_num))
		min_result.sort(key=lambda x: x[0], reverse=True)
		result = []
		for re in min_result:
			if re[0] > min_pro:
				result.append((re[0], self.topic_nwz[re[1]]))
		return result[:topic_num]

	def infer_sentence_topics(self, sentence, topic_num=1):
		sentence_biterms = self.SentenceProcess(sentence)

		topic_pro = [0] * self.topic_num
		# 短文本分析中，p (b|d) = nd_b/doc(nd_b)  doc(nd_b) 表示 计算的query 的所有biterm的计数
		# 因此，在short text 的p(b|d) 计算为1／biterm的数量
		bit_size = len(sentence_biterms)
		if not sentence_biterms:
			return None
		for bit in sentence_biterms:
			# cal p(z|d) = p(z|b)*p(b|d)
			# cal p(z|b)
			pz = [0] * self.topic_num
			self.compute_pz_b(bit, pz)
			pz_sum = sum(pz)
			pz = map(lambda pzk: pzk / pz_sum, pz)

			for x, y in zip(range(self.topic_num), pz):
				topic_pro[x] += y / bit_size

		result = topic_pro
		return result

	def reset_biterm(self, bit):
		k = bit.getTopic()
		w1 = int(bit.get_word()) - 1
		w2 = int(bit.get_word(2)) - 1

		self.nb_z[k] -= 1
		self.nwz[k][w1] -= 1
		self.nwz[k][w2] -= 1
		min_val = -(10 ** (-7))
		# if self.nb_z[k] > min_val and self.nwz[k][w1] > min_val and
		bit.resetTopic()

	def similarlyTopic(self, BitM):
		"""
		计算两个模型的相似话题映射
		:param BitM:
		:return:
		"""
		topic_list = []
		for topic in xrange(self.topic_num):
			min_sim = 0.0
			sim_topic_num = 0
			# print self.voca_size, BitM.voca_size
			min_voca_size = min(self.voca_size, BitM.voca_size)
			for b_topic in xrange(BitM.topic_num):
				sim = sum(map(lambda x, y: multiOper(x, y), self.nwz[topic], BitM.nwz[b_topic]))
				sum1 = sum(map(lambda x, y: x * y, self.nwz[topic][:min_voca_size], self.nwz[topic][:min_voca_size]))
				sum2 = sum(
					map(lambda x, y: x * y, BitM.nwz[b_topic][:min_voca_size], BitM.nwz[b_topic][:min_voca_size]))
				sim = sim / ((sum1 ** 0.5) * (sum2 ** 0.5))
				# print sim
				if sim > min_sim:
					sim_topic_num = b_topic
					min_sim = sim
			topic_list.append(sim_topic_num)
			print "topic :{} 的相似topic 是：{}, 相似度为：{}".format(topic, sim_topic_num, min_sim)
		topic_delength = len(list(set(topic_list)))
		print "话题对应比例：{}".format(float(topic_delength) / self.topic_num)

	def setAlpha(self, alpha=1.0):
		self.alpha = alpha

	def setBeta(self, beta=0.1):
		self.beta = beta


def multiOper(x, y):
	"""
	计算两个数的乘积，如果一个为0或不存在，则返回空
	:param x:
	:param y:
	:return:
	"""
	if x and y:
		return x * y
	else:
		return 0.0


def saveBTMModel(model, file=config.BTMData + "Model/BitModel_5.model"):
	with open(file, 'wb') as fp:
		pickle.dump(model, fp)


def loadBTMModel(file=config.BTMData + "Model/BitModel.model"):
	with open(file, 'rb') as fp:
		model = pickle.load(fp)
	return model


def recognize(BitM, test_file="test.txt", output=''):
	sentences = readTXTFile(test_file)

	result = []
	lab = []
	for sen in sentences:
		term = sen.strip().split("\t")
		# sen = sen.strip().replace(" ", '')
		i = 0
		if len(term) == 3:
			i = 1
		elif len(term) < 2 or len(term) > 3:
			continue
		else:
			pass
		topics = BitM.infer_sentence_topics(term[i])
		# print topics
		# if len(topic) == topic_num:
		# 	topic = topic[0]
		# else:
		# 	topic = (1.0, -1)
		if topics:
			result.append(topics)
			lab.append(term[i + 1])
	with codecs.open(output, "w", encoding="utf8") as fp:
		cPickle.dump([result, lab], fp)

	return result, lab


# fp.write(term[i] + "," + str(topic[0]) + "," + str(topic[1]) + "\t" + term[i + 1] + "\n")

def div_train_test(data, lab):
	n_samples = len(data)
	sidx = np.random.permutation(n_samples)
	valid_portion = 0.1
	n_train = int(np.round(n_samples * (1. - valid_portion)))
	test_set_x = [data[s] for s in sidx[n_train:]]
	test_set_y = [int(lab[s]) for s in sidx[n_train:]]
	train_set_x = [data[s] for s in sidx[:n_train]]
	train_set_y = [int(lab[s]) for s in sidx[:n_train]]
	return train_set_x, train_set_y, test_set_x, test_set_y


def predct_all(all_model, x, y):

	result = []
	st = True
	for one_x, one_y in zip(x, y):
		min_result = {}
		for model in all_model:
			lab = model.predict([one_x])[0]
			if lab in min_result:
				min_result[lab] += 1
			else:
				min_result[lab] = 1

		pre_lab = sorted(min_result.items(), key=lambda X: X[1], reverse=True)[0][0]
		if st:
			print pre_lab
			st = False
		result.append(pre_lab)
	return result



def naviBayes(train_X, train_y, test_X, test_y):
	# print train_y
	# print test_y
	# model = tfMultyPerceptron(train_X, train_y, test_X, test_y)
	# model.run()
	time_start = time.time()
	model = MLPClassifier(hidden_layer_sizes=(128, 32, 32, 128), max_iter=100, early_stopping=False, learning_rate_init=0.001,
	                      verbose=True)
	# model = MultinomialNB()
	# model = BernoulliNB()
	# model = KNeighborsClassifier()
	# model = DecisionTreeClassifier(max_depth=20, min_samples_leaf=0.01)
	# model = LinearSVC(random_state=0)
	# model.fit(X, y)
	model.fit(train_X, train_y)
	# model_1.fit(train_X, train_y)
	# model_2.fit(train_X, train_y)
	# model_3.fit(train_X, train_y)
	# model_4.fit(train_X, train_y)
	# model_5.fit(train_X, train_y)
	# All_model = [model, model_1, model_2, model_3, model_4, model_5]

	# train_pre = predct_all(All_model, train_X, train_y)
	# test_pre = predct_all(All_model, test_X, test_y)
	time_end = time.time()
	print "perceptron training cost time:{}".format(time_end - time_start)
	# model = OneVsRestClassifier(SVC(kernel='linear'))
	# model.fit(train_X, train_y)
	# save
	with open(config.BTMData + 'BayesModel/BTM_perceptron.model', 'wb') as fp:
		cPickle.dump(model, fp)

	# load model
	# model = None
	# with open(config.BTMData + 'BayesModel/bayes_BTM.model', 'rb') as fp:
	# 	model = cPickle.load(fp)

	# print 'train data set size:', len(train_y)
	# result = metrics.accuracy_score(train_pre, train_y)
	# 返回各自文本的所被分配到的类索引
	# print"Predicting random boost train result: ", result
	# print 'train data set size:', len(train_y)
	# result = metrics.accuracy_score(test_pre, test_y)
	# 返回各自文本的所被分配到的类索引
	# print "Predicting random boost test result:", result


	print 'train data set size:', len(train_y)
	result = model.score(train_X, train_y)
	# 返回各自文本的所被分配到的类索引
	print"Predicting train result: ", result

	test_result = model.score(test_X, test_y)
	print "Predicting test set result: ", test_result

	top_train_result = model.predict_proba(train_X)
	print "top 3 predict train data accuracy rate: {}".format(cal_topThreeScore(model, top_train_result, train_y))

	top_test_result = model.predict_proba(test_X)
	print "top 3 predict test data accuracy rate: {}".format(cal_topThreeScore(model, top_test_result, test_y))


def cal_topThreeScore(model, top_result, lab, top_num=3):
	count = len(lab)
	right_count = 0
	i = 0
	for topic_top, real_topic in zip(top_result, lab):
		topics = enumerate(topic_top)
		top_three = sorted(topics, key=lambda x: x[1], reverse=True)[:top_num]
		# print top_three

		three = [model.classes_[x[0]] for x in top_three]
		i += 1
		if real_topic in three:
			right_count += 1
	return float(right_count) / count


def analysis_topic():
	sentences = readTXTFile(config.BTMData + "analysis_result.txt")
	topic = {}
	for sen in sentences:
		term = sen.strip().split(",")
		if len(term) != 3:
			continue
		subterm = term[2].split("\t")
		if len(subterm) != 2:
			continue
		if subterm[1] in topic:
			if subterm[0] in topic[subterm[1]]:
				topic[subterm[1]][subterm[0]] += 1
			else:
				topic[subterm[1]][subterm[0]] = 1
		else:
			topic[subterm[1]] = dict()
			topic[subterm[1]][subterm[0]] = 1

	pro_right = 0.0
	pre_topic_list = []
	for key in topic:
		# topic[key] = list(set(topic[key]))
		topic_query_number = 0
		count = 0
		ana_topics = topic[key]
		max_val = 0
		max_topic = 0
		# print "zhihu topic : {} , analysis topic number:{}".format(key, len(ana_topics.keys()))
		for subkey in ana_topics:
			print "analysis topic id :{} ,频率: {}".format(subkey, ana_topics[subkey])
			topic_query_number += ana_topics[subkey]
			if max_val < ana_topics[subkey]:
				max_val = ana_topics[subkey]
				max_topic = subkey
		pro_right += max_val
		pre_topic_list.append(max_topic)

		for subkey in ana_topics:
			if ana_topics[subkey] > 0.05 * topic_query_number:
				count += 1
		print "zhihu topic : {} 's query number : {}\n high frequence topic number: {}".format(key, topic_query_number,
		                                                                                       count)
	rate = pro_right / len(sentences)
	print "all pre topic as follow:\n", " ".join(list(set(pre_topic_list))), "\ntopic number:", len(
		list(set(pre_topic_list)))
	return rate


def findBestParams():
	"""
	参数调优，参数优化 问题，通过测试寻找最优参数
	:return:
	"""
	best_alpha = 0.5
	best_beta = 0.1
	iter_times = 5
	best_rate = 0.0
	BitM = BtmModel(topic_num=100, iter_times=iter_times, alpha=best_alpha, beta=best_beta, has_background=False)
	BitM.Init_MOdel()
	for i in xrange(1, 10):
		for j in xrange(1, 20):
			alpha = i * 0.5
			beta = j * 0.1
			BitM.setAlpha(alpha)
			BitM.setBeta(beta)
			# BitM.preProcess()
			BitM.runModel()
			print BitM.nb_z
			recognize(BitM)
			rate = analysis_topic()
			if rate > best_rate:
				best_rate = rate
				best_alpha = alpha
				best_beta = beta
			print "迭代:{}次, alpha:{}, beta :{} 的 rate :{}".format(iter_times, alpha, beta, rate)
	print "best rate:{}, params (alpha: {}, beta: {})".format(best_rate, best_alpha, best_beta)
	return best_alpha, best_beta


def Analysis(alpha, beta):
	# BitM = BtmModel(topic_num=100, iter_times=10, alpha=alpha, beta=beta, has_background=False)
	# BitM.preProcess()
	# BitM.Init_MOdel()
	# alpha = (50 / float(BitM.topic_num))
	# beta = 200 / float(BitM.voca_size)
	# print "alpha:{}, beta:{}".format(alpha, beta)
	# BitM.setAlpha(alpha)
	# BitM.setBeta(beta)
	# BitM.runModel()
	# BitM.CombbineTopic()
	# saveBTMModel(BitM, config.BTMData + "Model/BitModel_100_vec.model")
	# BitM = loadBTMModel(config.BTMData + "Model/BitModel_100_10_2.model")
	# data, lab = recognize(BitM, "/Users/orion/PycharmProjects/Test2/Data/BTMData/sentence_P_topic_train.txt",
	#                       config.BTMData + "train.pkl")
	with codecs.open(config.BTMData + "train.pkl", "r") as fp:
		sdata = cPickle.load(fp)
		data, lab = sdata[0], sdata[1]
		train_X, train_y, test_X, test_y = div_train_test(data, lab)
		naviBayes(train_X, train_y, test_X, test_y)


# recognize(BitM, config.BTMData+"sentence_P_topic_test_1.txt", config.BTMData+"test.pkl")
# BitM = loadBTMModel(config.BTMData + "Model/BitModel_21_10_2.model")



# BitM.show()
# print BitM.topic_num
# print BitM.nb_z
# recognize(BitM, "sentence_P_topic_train.txt")
# tarin_rate = analysis_topic()
# print "train data rate:{}".format(tarin_rate)
# recognize(BitM, "sentence_P_topic_test.txt")
# test_rate = analysis_topic()
# print "train data rate:{},\t test data rate:{}".format(tarin_rate, test_rate)


def main():
	# alpha, beta = findBestParams()
	Analysis(alpha=0.98, beta=0.003)


if __name__ == "__main__":
	# buildTestFile()
	main()
