#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-08-03

import sys
sys.path.append("/home/mysql1/anqu/python/anquProduct/Server")
reload(sys)
import config

sys.setdefaultencoding('utf8') 

from HqlSpark import HqlSpark
from NetLink import NetLink
import json
from d9t.json import parser
from selectWord import selectWord
from Spark_means import Spark_means as skms

def runAnalysis(Appids,languadge='cn'):
	mysql = HqlSpark(languadge)
	nt = NetLink()
	spark_kmeans = skms()
	#get word using analysis
	mysql.getAllWord()
	all_AppIds,genre_Ids = nt.getCompleteIds(Appids)
	Matrix = mysql.getInPut(all_AppIds,genre_Ids)
	result = spark_kmeans.K_means(Matrix)
	print result



def main():
	runAnalysis(Appids=['1111484111','1012852987','1083354212','1097663377'])

if __name__ == '__main__':
	main()
