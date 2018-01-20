# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-10-24
# import sklearn.neighbors.class
import sys

sys.path.append('/Users/orion/PycharmProjects/Test2/MyCode')
reload(sys)
sys.setdefaultencoding('utf-8')
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import BaseNB
from scipy.sparse.coo import coo_matrix
# from scipy.sparse.csr import csr_matrix
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as Lda
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from minepy import MINE
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
from sklearn.cluster import MiniBatchKMeans
import cPickle
import config
import numpy as np
from sklearn import metrics
import jieba
import time

from sklearn.neural_network import MLPClassifier

def train_data_pre(train_x, train_y):
	topic_data = dict()
	print type(train_x)
	print train_x[0]
	print
	train_x = np.array(train_x.todense())
	for index in xrange(len(train_y)):
		y = train_y[index]
		if y in topic_data:
			topic_data[y].append(train_x[index])
		else:
			print train_x[index]
			print
			topic_data[y] = [train_x[index]]

	min_size = 100000
	for key in topic_data:
		length = len(topic_data[key])
		if length < min_size:
			min_size = length

	for key in topic_data:
		length = len(topic_data[key])
		if length > min_size:
			k_means = MiniBatchKMeans(n_clusters=min_size, init_size=int(3 * min_size))
			# print topic_data[key]
			print topic_data[key]
			k_means.fit(topic_data[key])
			topic_data[key] = k_means.cluster_centers_

def jieba_tokenize(text):
	return jieba.lcut(text)


def mic(x, y):
	m = MINE()
	print x
	print y
	m.compute_score(x, y)
	return (m.mic(), 0.5)


tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)
'''
	tokenizer: 指定分词函数
	lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
	所以最好是 False
'''
# text_list = ["今天天气真好啊啊啊啊", "小明上了清华大学",
#              "我今天拿到了 Google 的 Offer",
#              "清华大学在自然语言处理方面真厉害"]
#
train_data = []
lab = []
with open(config.BTMData + 'sentence_P_topic_train.txt', "r") as fp:
	for line in fp:
		term = line.strip().split('\t')
		if len(term) != 2:
			continue
		train_data.append(term[0])
		lab.append(term[1])

# tfidf_vectorizer.fit(train_data)
# save
# with open(config.BTMData+'BayesModel/tfidf_vectorizer.model', 'wb') as fp:
# 	cPickle.dump(tfidf_vectorizer, fp)

# load model
tfidf_vectorizer = None
load_start_time = time.time()
with open(config.BTMData + 'BayesModel/tfidf_vectorizer.model', 'rb') as fp:
	tfidf_vectorizer = cPickle.load(fp)
load_end_time = time.time()
print "load model cost time:{}".format(load_end_time - load_start_time)

n_samples = len(train_data)
print "data size:", n_samples
# shuffle and generate train and valid dataset
sidx = np.random.permutation(int(n_samples))

n_train = int(np.round(n_samples * (1. - 0.9)))
train_sentence = []
train_lab = []
test_sentence = []
test_lab = []
[train_sentence.append(train_data[s]) for s in sidx[n_train:]]
[train_lab.append(lab[s]) for s in sidx[n_train:]]
[test_sentence.append(train_data[s]) for s in sidx[:n_train]]
[test_lab.append(lab[s]) for s in sidx[:n_train]]

train_tfidf_matrix = tfidf_vectorizer.transform(train_sentence)

print train_tfidf_matrix.shape
feature = SelectKBest(chi2, k=10000)  # 卡方分布提取特征
# feature = SelectKBest(mutual_info_classif, k=10000)
feature.fit(train_tfidf_matrix, train_lab)

train_tfidf_matrix = feature.transform(train_tfidf_matrix)
test_tfidf_matrix = tfidf_vectorizer.transform(test_sentence)
test_tfidf_matrix = feature.transform(test_tfidf_matrix)
train_tfidf_matrix, train_lab = train_data_pre(train_tfidf_matrix, train_lab)

best_rate = 0
best_layer_num = 0
best_iter_num = 10
best_trian_rate = 0
with open(config.BTMData + "test_reult.txt", 'w') as fpw:
	for i in xrange(1):
		for j in xrange(1):
			# num_clusters = 20
			time_start = time.time()
			layer_num = 256
			max_iter_num = 100
			print "多层感知器，层数:{}, 神经元个数:{},迭代次数:{}".format(1, layer_num, max_iter_num)
			# model = MLPClassifier(hidden_layer_sizes=(layer_num,), learning_rate_init=0.0001, max_iter=max_iter_num, early_stopping=False, verbose=True)
			# model = Lda(solver="svd", store_covariance=True)
			# model = MultinomialNB()
			# model = KNeighborsClassifier(n_neighbors=5)
			# model = LinearSVC(random_state=0)
			model = DecisionTreeClassifier(splitter='random', max_depth=5000)
			print "start train ..."
			model.fit(train_tfidf_matrix, train_lab)
			time_end = time.time()
			print "train cost:{}s".format(time_end - time_start)
			# save
			with open(config.BTMData + 'BayesModel/MLPClassifier_1.model', 'wb') as fp:
				cPickle.dump(model, fp)

			print "finished train model and saving"

			# load model
			# model = None
			# with open(config.BTMData + 'BayesModel/MLPClassifier_1.model', 'rb') as fp:
			# 	model = cPickle.load(fp)

			fpw.write('train data set size:{}\n'.format(len(train_lab)))
			print 'train data set size:{}\n'.format(len(train_lab))
			result = model.score(train_tfidf_matrix, train_lab)
			# km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40,
			#                     init='k-means++', n_jobs=-1)

			# 返回各自文本的所被分配到的类索引
			# result = km_cluster.fit_predict(tfidf_matrix)
			fpw.write('Predicting train result:{}\n'.format(result))
			print"Predicting train result: ", result
			# with open("/Users/orion/PycharmProjects/Test2/Data/BTMData/analysis_result.txt", 'w') as fpw:
			# 	for sen, pre_topic, old_topic  in zip(train_sentence, result, lab):
			# 		fpw.write("{},0.0,{}\t{}\n".format(sen, pre_topic, old_topic))

			# print model.get_params()
			# print model.get_params(True)
			print "cal top three:... ..."
			top_result = model.predict_proba(train_tfidf_matrix)


			# print top_result[0]
			# model.classes_
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


			train_rate_top3 = cal_topThreeScore(model, top_result, train_lab)
			fpw.write("top 3 predict train data accuracy rate: {}\n".format(train_rate_top3))
			print "top 3 predict train data accuracy rate: {}".format(train_rate_top3)

			# 需要进行聚类的文本集
			fpw.write('test data set size:{}\n'.format(len(test_lab)))
			print 'test data set size:', len(test_lab)

			test_result = model.score(test_tfidf_matrix, test_lab)
			if best_rate < test_result:
				best_rate = test_result
				best_layer_num = layer_num
				best_iter_num = max_iter_num
				best_trian_rate = result
			fpw.write('Predicting test set result:{}\n'.format(test_result))
			print "Predicting test set result: ", test_result
			test_top_result = model.predict_proba(test_tfidf_matrix)

			test_rate_top3 = cal_topThreeScore(model, test_top_result, test_lab)
			fpw.write(
				"top 3 predict test data accuracy rate: {}".format(test_rate_top3))
			print "top 3 predict test data accuracy rate: {}".format(test_rate_top3)

	print "best rate:{},\nbest train rate:{},\nbest layer number:{},\nbest iter number:{}".format(best_rate,
	                                                                                              best_trian_rate,
	                                                                                              best_layer_num,
	                                                                                              best_iter_num)
	fpw.write("best rate:{},\nbest train rate:{},\nbest layer number:{},\nbest iter number:{}\n".format(best_rate,
	                                                                                                    best_trian_rate,
	                                                                                                    best_layer_num,
	                                                                                                    best_iter_num))

# print "precision:", metrics.precision_score()
# def main():
# 	bayes = Bayes()
# 	bayes.train()
#
#
# if __name__ == '__main__':
# 	main()
