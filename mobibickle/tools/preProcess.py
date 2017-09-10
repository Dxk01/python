# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-19

import time
from Code.tools.WriteResult import WriteResult
from Code.tools.ReadCsvFile import ReadCsvFile
from sklearn import preprocessing
import numpy


class PreProcess():
    def __init__(self):
        pass

    def preProcessTrainData(self,DataArrays):
        X = []
        Y = []
        loc_dic = {}
        index = 1
        for Data in DataArrays:
            len_items = len(Data)
            # Y.append(Data[len_items-1])
            data = []
            data.append(int(Data[3]))
            time_s = Data[4].split(" ")
            time_items = time_s[0].split("-")
            time_data_items = [int(x) for x in time_items]
            time_data_items.extend([0, 0, 0, 0, 0, 0])
            time_data_val = time.mktime(time_data_items)
            time_items.extend(time_s[1].split(":"))
            time_items = [int(x) for x in time_items]
            time_items.extend([0, 0, 0])
            time_val = time.mktime(time_items)
            time_val = time_val - time_data_val
            # print time_val
            loc_place = Data[5]
            if loc_dic.has_key(loc_place) == False:
                loc_dic[loc_place] = index
                index += 1
            loc_index = loc_dic[loc_place]
            data.append(time_val)
            data.append(loc_index)
            X.append(data)

            # 处理 Y
            des_loc_place = Data[6]
            if not loc_dic.has_key(des_loc_place):
                loc_dic[des_loc_place] = index
                index += 1
            Y.append(loc_dic[des_loc_place])
        wr = WriteResult()
        wr.WriteValueToFile(X,"trainData_X")
        wr.WriteValueToFile(Y,"trainData_Y")
        wr.WriteValueToFile(loc_dic,"train_loc_dic")
        return X,Y,loc_dic

    def preProcessTestData(self,DataArrays):
        X = []
        rf = ReadCsvFile()
        loc_dic = rf.ReadValueFromFile("train_loc_dic")
        index = len(loc_dic.keys())
        for Data in DataArrays:
            len_items = len(Data)
            data = []
            data.append(int(Data[3]))
            time_s = Data[4].split(" ")
            time_items = time_s[0].split("-")
            time_data_items = [int(x) for x in time_items]
            time_data_items.extend([0, 0, 0, 0, 0, 0])
            time_data_val = time.mktime(time_data_items)
            time_items.extend(time_s[1].split(":"))
            time_items = [int(float(x)) for x in time_items]
            time_items.extend([0, 0, 0])
            time_val = time.mktime(time_items)
            time_val = time_val - time_data_val
            # print time_val
            loc_place = Data[5]
            if loc_dic.has_key(loc_place) == False:
                loc_dic[loc_place] = index
                index += 1
            loc_index = loc_dic[loc_place]
            data.append(time_val)
            data.append(loc_index)
            X.append(data)

        wr = WriteResult()
        wr.WriteValueToFile(X, "testData_X")
        wr.WriteValueToFile(loc_dic, "test_loc_dic")
        return X, loc_dic

    def getFeatureScaler(self,X):
        max_min_scaler = preprocessing.MinMaxScaler()
        train_XM = numpy.array(X)
        train_Xc = max_min_scaler.fit_transform(train_XM)
        return train_Xc