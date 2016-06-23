#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-23

import sys
sys.path.append("/home/spark/anqu/code/data_deal")
sys.path.append("/home/spark/anqu/code/Tools")
sys.path.append("/home/spark/anqu/code/wordAnalysis")
reload(sys)
sys.setdefaultencoding('utf8') 

import mysql_op
import data_deal
import calculSimilarity

class selectWord():
	"""docstring for ClassName"""
	def __init__(self):
		self.my_data = data_deal.data_deal()
	def print_line(self,x,y,z):
		print x[0],x[1],x[2],y,z
	def selectWord(self):
		data = self.my_data.getWordPrioandSearchC()
		similarity,resault = calculSimilarity.similarity().run()
		# print len(data)
		# print len(similarity)	
		map(lambda x,y,z: self.print_line(x,y,z),data,similarity,resault)

def main():
	SelectWord = selectWord()
	SelectWord.selectWord()

if __name__ == '__main__':
	main()
