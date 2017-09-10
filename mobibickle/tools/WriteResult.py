# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-18

import Config
import pickle

"""结果写入文件"""

class WriteResult():
    def __init__(self,BasedPath=Config.ResultDataPath):
        self.BasedPath = BasedPath

    def WriteValueToFile(self,model,file="Data_X"):
        file = Config.ResultDataPath+file+".model"
        with open(file,'wb') as fp:
            pickle.dump(model,fp)

    def WriteResultAnswer(self,pre_data=None,pre_anwser=None,file=None):
        if not file:
            file = Config.ResultDataPath+"result.csv"
        add = None
        print "answer:",len(pre_anwser),"data:",len(pre_data)
        length = 0
        if len(pre_data) <= len(pre_anwser):
            length = len(pre_data)
        else:
            length = len(pre_anwser)

        with open(file,"a+") as fp:
            # fp.write("orderid,geohashed_end_loc1,geohashed_end_loc2,geohashed_end_loc3")
            for i in xrange(length):
                # print i,pre_data[i][0]
                # print pre_anwser[i]
                fp.write(pre_data[i][0]+","+pre_anwser[i][0]+","+pre_anwser[i][1]+","+pre_anwser[i][2]+"\n")
