# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-18

from Code.tools import Config
import time
from Code.tools.WriteResult import WriteResult
from Code.tools.ReadCsvFile import ReadCsvFile
from Code.tools.preProcess import PreProcess
from sklearn import preprocessing
import numpy

class MyTest():
    def __init__(self):
        pass

    def TestReadFile(self):
        # rcf = ReadCsvFile()
        # start_r = time.time()
        # trainData = rcf.ReadTrainFile()
        # end_t = time.time()
        # print "read train data cost time :",(end_t-start_r)
        # print len(trainData)
        # for re in trainData:
        #     print re
        # start_r = time.time()
        # testData = rcf.ReadTestFile()
        # end_t = time.time()
        # print "read test data cost time :", (end_t - start_r)
        # for re in testData:
        #     print re
        wr = WriteResult()
        rf = ReadCsvFile()
        train_X = rf.ReadValueFromFile("trainData_X")
        train_Y = rf.ReadValueFromFile("trainData_Y")
        train_loc_dic = rf.ReadValueFromFile("train_loc_dic")
        # print len(testData)
        max_min_scaler = preprocessing.MinMaxScaler()
        train_XM = numpy.array(train_X)
        train_Xc = max_min_scaler.fit_transform(train_XM)

        wr.WriteValueToFile(train_Xc,)
        print train_Xc

        preProce = PreProcess()
        # test_X,test_loc_dic = preProce.preProcessTestData(testData)
        test_X = rf.ReadValueFromFile("testData_X")
        test_loc_dic = rf.ReadValueFromFile("test_loc_dic")
        # X,Y,loc_dic = preProce.preProcess(trainData)
        print "X size:",len(test_X)
        print test_X[0],len(test_loc_dic.keys())
        # for i in xrange(len(X)):
        test_XM = numpy.array(test_X)
        test_Xc = max_min_scaler.fit_transform(test_XM)
        print
        print test_Xc




def main():
    mt = MyTest()
    mt.TestReadFile()


if __name__ == '__main__':
    main()