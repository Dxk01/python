# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-18

from sklearn.naive_bayes import GaussianNB
from Code.tools.WriteResult import WriteResult
from Code.tools.ReadCsvFile import ReadCsvFile
from Code.tools.preProcess import PreProcess
from tools import Config
from multiprocessing import cpu_count
import threading
import threadpool
import time
import logging

logging.basicConfig(filename=Config.ResultDataPath+'logger.log',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

mu = threading.Lock()

def TrainModel(train_data,train_lab):
    model = GaussianNB()
    model.fit(train_data,train_lab)
    wr = WriteResult()
    wr.WriteValueToFile(model,"predict_Model")
    return model

def LoadModel(model_name="predict_Model"):
    model = None
    rf = ReadCsvFile()
    model = rf.ReadValueFromFile(model_name)
    predict_result = None
    if model:
        # predict_result = model.predict_proba(test_data)
        print "Load Model success!"
    else:
        train_data = rf.ReadTrainFile()
        preProce = PreProcess()
        train_X,train_lab,train_loc_dic = preProce.preProcessTrainData(train_data)
        train_Xc =preProce.getFeatureScaler(train_data)
        model = TrainModel(train_Xc,train_lab)
        # predict_result = model.predict_proba(test_data)
    return model

def predict(model,test_data):
    return model.predict_proba(test_data)

def find_min_index(topThree):
    min_index = 0
    for i in xrange(len(topThree)):
        if topThree[i] < topThree[min_index]:
            min_index = i
    return min_index

def setHeep():
    pass

def transformResult(pre_result=None,loc_dic=None):
    if not len(pre_result):
        return
    final_result = []
    # 找到最大可能三个地方的索引
    line_result = []
    place_list = sorted(loc_dic.iteritems(), key=lambda X: X[1])
    for result in pre_result:
        # print("result size:%d"%len(result))
        topThree = []
        for i in xrange(3):
            topThree.append((result[i],i))
        # min_index = 0
        for j in xrange(3,len(result)):
            topThree = sorted(topThree,key=lambda X:X[0],reverse=False)
            min_index = find_min_index(topThree)
            if result[j] > topThree[0][0]:
                topThree[0] = (result[j],j)
        topThree = sorted(topThree,key=lambda  X:X[0],reverse=True)
        line_result.append(topThree)

    for topThree in line_result:
        for index in topThree:
            print index
            try:
                line_result.append(place_list[index[1]][0])
            except:
                print index
                # print place_list
        final_result.append(line_result)
    return final_result

def threadPredict(model,test_data,test_Xc,start_index,end_index,test_loc_dic):
    start_time = time.time()
    pre_result = predict(model, test_Xc[start_index:end_index])
    end_time = time.time()

    print "predict from %d to %d. \n cost time :%lf s\n" % (start_index, end_index, end_time - start_time)
    start_time1 = time.time()
    result = transformResult(pre_result, test_loc_dic)
    if mu.acquire(True):
        wr = WriteResult()
        wr.WriteResultAnswer(test_data[start_index:end_index], result,Config.ResultDataPath+"submission_1.csv")
        mu.release()
    end_time1 = time.time()
    print "transform index from %d to %d. \n cost time :%lf s\n" % (start_index, end_index, end_time1 - start_time1)

def mulThreadpredict(test_data,model,start_index_lab=270):
    preP = PreProcess()
    test_X, test_loc_dic = preP.preProcessTestData(test_data)
    test_Xc = preP.getFeatureScaler(test_X)
    test_X = None
    length = len(test_Xc)
    # 初始化线程池
    print "cpu number:", cpu_count()
    cpus = cpu_count()
    pool = threadpool.ThreadPool(cpus-1)
    print "test data len:", length
    print "predict result ... ... "
    list_args = []
    for i in xrange(start_index_lab, length):
        pre_result = None
        start_index = i * 1000
        end_index = (i + 1) * 1000
        if end_index > length:
            end_index = length
        args = [model,test_data,test_Xc,start_index,end_index,test_loc_dic]
        list_args.append((args,None))
    requests = threadpool.makeRequests(threadPredict, list_args)
    [pool.putRequest(req) for req in requests]
    pool.wait()




def main():
    print "Start......"
    rf = ReadCsvFile()
    # train_data = rf.ReadTrainFile()
    preP = PreProcess()
    # train_X,train_lab,loc_dic = preP.preProcessTrainData(train_data)
    # train_Xc = preP.getFeatureScaler(train_X)
    # print "Train model"
    # TrainModel(train_Xc,train_lab)
    # train_lab = None
    # loc_dic = None
    # train_data = None
    # train_X = None
    # train_Xc = None
    # with open(Config.ResultDataPath+"result.csv","w") as fp:
    #     print "清空文件","result.csv"
    model = LoadModel()
    # print "Read data predict ... ... "
    test_data = rf.ReadTestFile()
    test_X,test_loc_dic = preP.preProcessTestData(test_data)
    test_Xc = preP.getFeatureScaler(test_X)
    test_X = None
    length = len(test_Xc)
    print "test data len:",length
    print "predict result ... ... "
    for i in xrange(104,length):
        pre_result = None
        start_index = i * 100
        end_index = (i+1) * 100
        if end_index > length:
            end_index = length
        start_time = time.time()
        pre_result = predict(model,test_Xc[start_index:end_index])
        end_time = time.time()
        print "predict from %d to %d. \n cost time :%lf s\n" % (start_index, end_index,end_time-start_time)
        start_time = time.time()
        result = transformResult(pre_result, test_loc_dic)
        logging.info("predict from %d to %d. \ncost time :%lf s" % (start_index, end_index,end_time-start_time))
        wr = WriteResult()
        wr.WriteResultAnswer(test_data[start_index:end_index], result,Config.ResultDataPath+"result_1.csv")
        end_time = time.time()
        logging.info("transform index from %d to %d. \ncost time :%lf s" % (start_index, end_index,end_time-start_time))
        print "transform index from %d to %d. \n cost time :%lf s\n" % (start_index, end_index,end_time-start_time)

if __name__ == "__main__":
    main()