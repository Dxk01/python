# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-18

import Config
import pickle


class ReadCsvFile():
    def __init__(self):
        self.TrainFile = Config.TrainDataPath + 'train.csv'
        self.TestFile = Config.TestDataPath + 'test.csv'

    def ReadTrainFile(self,file=None):
        if file != None:
            self.TrainFile = file
        DataArray = []
        with open(self.TrainFile,"r") as fp:
            # 读 列表项目名
            fp.readline()
            # for test
            # i = 0
            # 读 数据
            line = None
            line = fp.readline()
            while line:
                items = line.strip().split(",")
                if len(items) != 7:
                    continue
                # for test
                # i += 1
                # if  i >= 100:
                #     break
                DataArray.append(items)
                line = fp.readline()
        return DataArray

    def ReadTestFile(self,file=None):
        if file != None:
            self.TestFile = file
        DataArray = []
        with open(self.TestFile, "r") as fp:
            # 读 列表项目名
            fp.readline()
            # for test
            # i = 0
            # 读 数据
            line = None
            line = fp.readline()
            while line:
                items = line.strip().split(",")
                if len(items) != 6:
                    continue
                # for test
                # i += 1
                # if i >= 100:
                #     break
                DataArray.append(items)
                line = fp.readline()
        return DataArray

    def ReadValueFromFile(self,file="trainData_X"):
        file = Config.ResultDataPath+file+".model"
        model = None
        with open(file,'rb') as fp:
            try :
                model = pickle.load(fp)
            except Exception,e:
                model = None
            # finally:
            #     model = None
        return model
