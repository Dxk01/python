# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-10-09
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from MyCode import config
# from MyCode.tools.filterStopWords import filterStopWords
import codecs
# from MyCode.tools.Participle import Participle
import jieba
from MyCode.tools.filterStopWords import filterStopWords

def buildData(file=config.QueryPath+"AllQueriesWithID.txt"):
	"""
	读取源数据文件，生成分析需要的语料
	:param file: 文件名
	:return:
	"""
	result_fp = codecs.open(config.BTMData+"btm_text_corpus_2000.txt", 'w', encoding='utf8')
	with codecs.open(file, 'r', encoding='utf8') as fp:
		for line in fp:
			if len(line) < 5:
				continue
			term = line.strip().split("\t")[1]
			term = term.split(' ')
			if term:
				result_fp.write(" ".join(term)+"\n")

	result_fp.close()

def buildData_corpus(file=config.BTMData+"document_corpus_2000.txt"):
	"""
	query 分词和过滤停用词
	:param file: 文件路径
	:return:
	"""
	result_fp = codecs.open(config.BTMData+"btm_text_corpus.txt", 'w', encoding='utf8')
	with codecs.open(file, 'r', encoding='utf8') as fp:
		for line in fp:
			line = line.strip()
			term = jieba.cut(line)
			if term:
				result_fp.write(" ".join(filterStopWords(term))+"\n")
	result_fp.close()

def getData(file=config.BTMData+'sentence_P_topic_train_1.txt'):
	topic_num = 0
	topic = {}
	sentences = []
	documents = []
	topic_sen = {}
	with codecs.open(file, 'r', encoding='utf8') as fp:
		for line in fp:
			line = line.strip()
			term = line.split("\t")
			if len(term) != 3:
				continue
			if term[2] not in topic:
				topic_num += 1
				topic[term[2]] = topic_num
				topic_sen[term[2]] = []
			sentences.append("\t".join(term[1:])+"\n")
			topic_sen[term[2]].append(term[1].strip())
			doc = " ".join(jieba.cut(term[1]))
			documents.append(doc+"\n")

		with codecs.open(config.BTMData+"sentence_and_topic.txt", 'w', encoding='utf8') as fp:
			# print "corpus size >= 2000:", len(topic_sen.keys())
			count = 0
			for topic in topic_sen:
				# if len(topic_sen[topic]) >= 1500:
				# 	count += 1
				for sen in topic_sen[topic]:
					fp.write("{}\t{}\n".format(sen.strip(), topic))
			# print "corpus size >= 2000:", count
		with codecs.open(config.BTMData+"document_corpus.txt", 'w', encoding="utf8") as fp:
			for topic in topic_sen:
				# if len(topic_sen[topic]) >= 1500:
				for sen in topic_sen[topic]:
					fp.write("{}\n".format(sen.strip()))
		print "topic number :{}".format(topic_num)

def proData(file="/Users/orion/PycharmProjects/Test2/Data/BTMData/sentence_P_topic_train.txt"):
	topic_num = 0
	topic = {}
	sentences = []
	documents = []
	topic_sen = {}
	with codecs.open(file, 'r', encoding='utf8') as fp:
		sentence = {}
		for line in fp:
			line = line.strip()
			term = line.split("\t")
			if len(term) != 2:
				continue
			if term[1] not in topic:
				topic_num += 1
				topic[term[1]] = topic_num
				topic_sen[term[1]] = []
			if term[0] in sentence:
				continue
			sentence[term[0]] = term[1]
			sentences.append("\t".join(term) + "\n")
			topic_sen[term[1]].append(term[0].strip())
			doc = " ".join(jieba.cut(term[0]))
			documents.append(doc + "\n")

	with codecs.open(config.BTMData + "sentence_and_topic.txt", 'w', encoding='utf8') as fp:
		# print "corpus size >= 2000:", len(topic_sen.keys())
		count = 0
		for topic in topic_sen:
			for sen in topic_sen[topic]:
				fp.write("{}\t{}\n".format(sen.strip(), topic))
	with codecs.open(config.BTMData + "document_corpus.txt", 'w', encoding="utf8") as fp:
		for topic in topic_sen:
			for sen in topic_sen[topic]:
				fp.write("{}\n".format(sen.strip()))
	print "topic number :{}".format(topic_num)

def main():
	proData('/Users/orion/PycharmProjects/Test2/Data/BTMData/sentence_P_topic_train.txt')
	buildData_corpus(config.BTMData+"document_corpus.txt")

if __name__ == '__main__':
	main()
