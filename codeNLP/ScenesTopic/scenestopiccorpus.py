# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-23

from MyCode import config
import xlrd


def readCorpus(file=config.ScenesTopicPath+"scenesTopic0923.xlsx"):
	bk = xlrd.open_workbook(file)
	table_names = bk.sheet_names()
	return bk, table_names

def getContext(bk,tableName='help'):
	



if __name__ == "__main__":
	 bk,table_name = readCorpus()
	 print table_name[1]
