#_*_ coding:utf-8 _*_
# Writor: lgy
# datetime: lgy

import os
import jieba
import pickle as pkl
from tflearn.data_utils import pad_sequences
import numpy as np


# load data
def loadData(dir="/Users/orion/PycharmProjects/Test2/MyCode/xiaomiScrip/history"):
	if not os.path.exists(dir):
		print("{} not exists".format(dir))

	files = os.listdir(dir)
	query = []
	response = []
	for f in files:
		if (os.path.isdir(dir + "/" + f)):
			continue

		with open(dir + "/" + f, "r") as fp:
			for line in fp:
				term = line.strip().split("\t")
				if len(term) == 2:
					query.append(term[0])
					response.append(term[1])

	return query, response

# fenci
def fenci(query, response):
	query_word = []
	response_word = []
	word_id = {}
	id_word = {}
	index = 1
	q_max_len = 0
	r_max_len = 0
	for q, r in zip(query, response):
		q_words = jieba.cut(q)
		q_w_id = []
		for w in q_words:
			if w not in word_id:
				word_id[w] = index
				id_word[index] = w
				index += 1
			q_w_id.append(word_id[w])
		q_max_len = max(q_max_len, len(q_w_id))
		query_word.append(q_w_id)
		r_w_id = []
		r_word = jieba.cut(r)
		for w in r_word:
			if w not in word_id:
				word_id[w] = index
				id_word[index] = w
				index += 1
			r_w_id.append(word_id[w])
		r_max_len = max(r_max_len, len(r_w_id))
		response_word.append(r_w_id)
	# 结果存储
	with open("word_id.pkl", "w") as fp:
		pkl.dump(word_id, fp)

	with open("id_word.pkl", "w") as fp:
		pkl.dump(id_word, fp)

	with open("query_response_id.txt", "w") as fp:
		for q, r in zip(query_word, response_word):
			fp.write("{}\t{}\n".format(" ".join(map(str, q)), " ".join(map(str, r))))

	return q_max_len, r_max_len, query_word, response_word, index

def load_dic(file="xiaomi_dict.txt"):
	word_id = {}
	id_word = {}
	with open(file, "r") as fp:
		for line in fp:
			term = line.strip().split("\t")
			if len(term) == 2:
				word_id[term[0]] = int(term[1])
				id_word[term[1]] = term[0]
	return word_id, id_word, len(word_id.keys())+1

def load_data(file="xiaomi_sent_2_sent.txt"):
	query, response = [], []
	q_max_len = 0
	r_max_len = 0
	with open(file, "r") as fp:
		for line in fp:
			term = line.strip().split("\t")
			if len(term) == 2:
				q = map(int, term[0].split(" "))
				q_max_len = max(q_max_len, len(q))
				r = map(int, term[1].split(" "))
				r_max_len = max(r_max_len, len(r))
				query.append(q)
				response.append(r)

	return query, response, q_max_len, r_max_len


def pad_SentencesQR(query, response):
	q_max_len, r_max_len, query_word, response_word, index = fenci(query, response)
	print("query max length:{}, response max length:{}".format(q_max_len, r_max_len))
	train_query = pad_sequences(query_word, maxlen=q_max_len, value=index)
	train_response = pad_sequences(response_word, maxlen=r_max_len, value=index)
	# print train_query[0]
	# print train_response[0]
	train_query = np.array(train_query)
	train_response = np.array(train_response)
	train_query_response = np.append(train_query, train_response, axis=1)
	return train_query, train_query_response, train_response, q_max_len, r_max_len, index

def pad_sentences_qr(query, response, q_max_len, r_max_len, index):
	train_query = pad_sequences(query, maxlen=q_max_len, value=index)
	train_response = pad_sequences(response, maxlen=r_max_len, value=index)
	train_query = np.array(train_query)
	train_response = np.array(train_response)
	train_query_response = np.append(train_query, train_response, axis=1)
	return train_query, train_query_response, train_response, q_max_len, r_max_len, index+1

# query, response = loadData()
# train_query, train_query_response, train_response, q_max_len, r_max_len = pad_SentencesQR(query, response)
# print train_query_response[0]
# print train_response[0]
