#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-24

import sys
sys.path.append("/home/spark/anqu/code/data_deal")
sys.path.append("/home/spark/anqu/code/Tools")
sys.path.append("/home/spark/anqu/code/wordAnalysis")
reload(sys)
sys.setdefaultencoding('utf8') 

import mysql_op

class selectWord():
	def __init__(self):
		self.mysql = mysql_op.mysql_op()

	#获取各类簇最大词热的word
	def selectMaxPriorityofCluster(self):
		max_priority = self.mysql.getWordPriority("select max(priority),cluster from wordSelectFeature group by cluster")
		max_prio_re = []
		# print max_priority
		for line in max_priority:
			sql = "select word,priority,cluster from wordSelectFeature where priority = %d and cluster = %d"%line
			data = self.mysql.select(sql)
			max_prio_re.append(data)
		return max_prio_re

	#获取当前词热前K大的word
	def selectTopKMaxPriority(self,K):
		sql = "select word,priority,cluster from wordSelectFeature order by priority desc limit %d"%K
		# print sql
		max_priority_re = self.mysql.getWordPriority(sql)
		return max_priority_re

	#获取当前热词前K小的word
	def selectTopKMinPriority(self,K):
		sql = "select word,priority,cluster from wordSelectFeature order by priority asc limit %d"%K
		min_priority_re = self.mysql.getWordPriority(sql)
		return min_priority_re

	# 获取当前各类簇的词热最小的word
	def selectMinPriorityofCluster(self):
		min_priority = self.mysql.getWordPriority("select min(priority),cluster from wordSelectFeature group by cluster")
		min_prio_re = []
		# print min_priority
		for line in min_priority:
			sql = "select word,priority,cluster from wordSelectFeature where priority = %d and cluster = %d"%line
			data = self.mysql.select(sql)
			min_prio_re.append(data)
		return min_prio_re

	# 获取当前词中的searchCount最大的Top K
	def selectTopKMaxSearchCount(self,K):
		sql = "select word,searchCount,cluster from wordSelectFeature order by searchCount desc limit %d"%K
		# print sql
		max_searchCount_re = self.mysql.getWordPriority(sql)
		return max_searchCount_re

	#获取当前词中的searchCount最小的Top K 
	def selectTopKMinSearchCount(self,K):
		sql = "select word,searchCount,cluster from wordSelectFeature order by searchCount asc limit %d"%K
		min_searchCount_re = self.mysql.getWordPriority(sql)
		return min_searchCount_re

	# 获取当前词中各类簇中searchCount最大的word
	def selectMinSerachCountOfCluster(self):
		min_searchCount_re = self.mysql.getWordPriority("select min(searchCount),cluster from wordSelectFeature group by cluster")
		min_searchCount_word = []
		for line in min_searchCount_re:
			sql = "select word,searchCount,cluster  from wordSelectFeature where searchCount = %d and cluster = %d"%line
			data = self.mysql.getWordPriority(sql)
			min_searchCount_word.append(data[0])
		return min_searchCount_word

	# 获取当前词中各类簇中searchCount最大的 Top K
	def selectMaxSearchCountOfCluster(self):
		max_searchCount_re = self.mysql.getWordPriority("select max(searchCount),cluster from wordSelectFeature group by cluster")
		print 
		max_searchCount_word = []
		for line in max_searchCount_re:
			sql = "select word,searchCount,cluster  from wordSelectFeature where searchCount = %d and cluster = %d"%line
			data = self.mysql.getWordPriority(sql)
			max_searchCount_word.append(data[0])
		return max_searchCount_word

def main():
	SelectWord = selectWord()
	# word_list = SelectWord.selectMaxPriority()
	# word_list = SelectWord.selectTopKMinPriority(10)
	# word_list = SelectWord.selectMinPriorityofCluster()
	word_list = SelectWord.selectMaxSearchCountOfCluster()
	for word in word_list:
		print word[0],word[1],word[2]
		pass

if __name__ == '__main__':
	main()