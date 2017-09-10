# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-26

import sys
sys.path.append("../")
reload(sys)
from tools.ReadCsvFile import ReadCsvFile
from tools.preProcess import PreProcess
from sklearn.svm import SVC
from tools.WriteResult import WriteResult
import logging
from tools import Config
import time


logging.basicConfig(filename=Config.ResultDataPath+'logger.log',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

rf = ReadCsvFile()
train_data = rf.ReadTrainFile()
preP = PreProcess()
train_X,train_lab,loc_dic = preP.preProcessTrainData(train_data)
train_Xc = preP.getFeatureScaler(train_X)

def TrainModel(modelName='SvmModel_2'):
	svm_model = None
	try:
		svm_model = ReadCsvFile.ReadValueFromFile(modelName)
		logging.info("load model success")
	except:

		print "Train model"
		logging.info("Train model")
		svm_model = SVC(decision_function_shape="ovo")
		# for i in xrange(len(train_data)/1000+1):
		i = 0
		start_index = i*10000
		end_index = (i+2)*10000
		# if end_index >= len(train_data):
		# 	end_index = len(train_data)
		svm_model.fit(train_Xc[start_index:end_index],train_lab[start_index:end_index])
		print svm_model.get_params()
			# if end_index == len(train_data):
			# 	break
		print "save model"
		logging.info("save model")
		wr = WriteResult()
		wr.WriteValueToFile(svm_model,modelName)
		print "精确度为: {0}".format(svm_model.score(train_Xc[end_index-1000:end_index],train_lab[end_index-1000:end_index]))
	return svm_model

model = TrainModel()

def topindex(result,topn=3):
	indexs = {}
	for i in xrange(topn):
		for j in xrange(len(result)):
			if j in indexs:
				continue
			else:
				if len(indexs.keys()) == 3:
					for index in indexs:
						print index,indexs[index],";",
					print
					min_index = min(indexs.iteritems(),key=lambda X:X[1])
					# print min_index
					if result[j] > result[min_index[0]]:
						indexs.pop(min_index[0])
						indexs[j] = result[j]
				else:
					indexs[j] = result[j]

	return indexs.keys()

# for test
def score():
	print "start caculate rate... ..."
	result_X = model.predict_proba(train_Xc[10000:11000])
	labs = train_lab[10000:11000]
	right = 0
	for i in xrange(len(labs)):
		# print result_X[i]
		result = topindex(result_X[i])
		print result
		if labs[i] in result:
			right += 1
	print right
	print "精确率：{0}".format(float(right)/len(labs))

def predict(model):
	rf = ReadCsvFile()
	preP = PreProcess()
	print "Read data predict ... ... "
	test_data = rf.ReadTestFile()
	test_X,test_loc_dic = preP.preProcessTestData(test_data)
	test_Xc = preP.getFeatureScaler(test_X)
	test_X = None
	length = len(test_Xc)
	print "test data len:",length
	print "predict result ... ... "
	for i in xrange(0,length):
		# pre_result = None
		start_index = i * 100
		end_index = (i+1) * 100
		if end_index > length:
			end_index = length
		start_time = time.time()
		# pre_result = predict(model,test_Xc[start_index:end_index])
		pre_result = model.predict_proba(test_Xc[start_index:end_index])

		end_time = time.time()
		for re in pre_result:
			print re
		# print "predict from %d to %d. \n cost time :%lf s\n" % (start_index, end_index,end_time-start_time)
		# start_time = time.time()
		# result = Process.transformResult(pre_result, test_loc_dic)
		# logging.info("predict from %d to %d. \ncost time :%lf s" % (start_index, end_index,end_time-start_time))
		# wr = WriteResult()
		# wr.WriteResultAnswer(test_data[start_index:end_index], result,Config.ResultDataPath+"result_d_1.csv")
		# end_time = time.time()
		# logging.info("transform index from %d to %d. \ncost time :%lf s" % (start_index, end_index,end_time-start_time))
		# print "transform index from %d to %d. \n cost time :%lf s\n" % (start_index, end_index,end_time-start_time)

# predict(model)


