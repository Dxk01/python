#encodig=utf-8
# Writer : lgy
# dateTime : 2018-07-27

import sys
import pandas as pd
def loaddata(file="Data/SourceData/train.csv", batch_size=1):
    with open(file, "r") as fp:
        lines = fp.readlines(8182*batch_size)
        # print(lines[0])
        lines = lines[1:]
        while lines:
            datas = []
            for line in lines:
                datas.append(line.strip().split(","))
            yield datas
            lines = fp.readlines(8182*batch_size)
        return None


# print(loaddata()[:10])
# data_iter = loaddata()
# data = next(data_iter)
# i = 0
# while data:
#     print(len(data))
#     print("\n")
#     for line in data:
#         print(line)
#     # print(data)
#     data = next(data_iter)
#     i += 1
#     if i >= 1:
#         break
# print(data)
