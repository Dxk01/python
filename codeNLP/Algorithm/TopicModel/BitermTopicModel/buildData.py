# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-10-09

from MyCode import config
from MyCode.tools.filterStopWords import filterStopWords
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
	result_fp = codecs.open("btm_text_corpus.txt", 'w', encoding='utf8')
	with codecs.open(file,'r',encoding='utf8') as fp:
		for line in fp:
			if len(line) < 5:
				continue
			term = line.strip().split("\t")[1]
			term = filterStopWords(term.split(' '))
			result_fp.write(" ".join(term)+"\n")

	result_fp.close()


def getData(file=config.TopicFilePath+'topic_questions_v2.csv'):
	topic_num = 0
	topic = {}
	sentences = []
	documents = []
	with codecs.open(file, 'r', encoding='utf8') as fp:
		for line in fp:
			line = line.strip()
			term = line.split("\t")
			if len(term) != 3:
				continue
			if term[2] not in topic:
				topic_num += 1
				topic[term[2]] = topic_num
			sentences.append("\t".join(term[1:])+"\n")
			doc = " ".join(filterStopWords(jieba.cut(term[1])))
			documents.append(doc+"\n")

		with codecs.open("sentence_and_topic.txt", 'w' ,encoding='utf8') as fp:
			for sen in sentences:
				fp.write(sen)

		with codecs.open("document_corpus.txt", 'w', encoding='utf8') as fp:
			for doc in documents:
				fp.write(doc)
		print "topic number :{}".format(topic_num)



def main():
	# buildData()
	getData()



if __name__ == '__main__':
	main()
