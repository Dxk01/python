#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-08-02

import sys
sys.path.append('/home/mysql1/anqu/python/anquProduct/Server')
sys.path.append('/home/mysql1/anqu/python/anquProduct/Server/RecieveFileData')
reload(sys)
sys.setdefaultencoding('utf8')
import config
# from file_op import file_op
from HqlSpark import HqlSpark
from pyspark import SparkConf
from pyspark import SparkContext

class selectWord():
	def __init__(self):
		self.myHql = HqlSpark()
		# self.conf = SparkConf().setAppName('selectWord')
		# self.sc = SparkContext(conf=self.conf)
		# self.
	# according input word get think word
	def getThinkWord(self,base_words):
		

def main():
	sw = selectWord()

if __name__ == '__main__':
	main()
