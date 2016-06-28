#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-22

import sys
sys.path.append("/home/spark1/python/")
sys.path.append("/home/spark/anqu/python/code")
reload(sys)
sys.setdefaultencoding('utf8') 
import jieba

class participle():
	def __init__(self):
		pass

	def participleWord(self,sentence):
		sen = sentence.decode('utf-8')[0:8].encode('utf-8')
		return list(jieba.cut(sen,cut_all=True))

	def participleCluster(self,cluster_resaults):
		word_list = []
		for sentence in cluster_resaults:
			word_list.extend(self.participleWord(sentence))
		return word_list

def main():
	str_1 = '词的标签：每个词均有自己的genreID标签集合，根据标签的重要性可以确定词的重要性'
	participleW = participle()
	# participleW.participleWord(str_1)
	for word in participleW.participleWord(str_1):
		print word,len(word)
	# print str_1

if __name__ == '__main__':
	main()