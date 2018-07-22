# _*_ coding:utf8 _*_
'''
Pedagogical example realization of seq2seq recurrent neural networks, using TensorFlow and TFLearn.
More info at https://github.com/ichuang/tflearn_seq2seq
'''

from __future__ import division, print_function

import sys
# sys.setdefaultencoding('utf-8')
class DataLoad():

    def __init__(self):
        pass

    def load_data(self, file="data.txt"):
        data = []
        with open(file, "r") as fp:
            line = fp.readline()
            while line:
                terms = line.split(" ")
                id = terms[0]
                values = terms[2:9]
                int_values = []
                for v in values:
                    int_values.append(int(v))
                # print(id, int_values)
                data.append((id, int_values))
                line = fp.readline()

        all_data = []
        print(len(data))
        for j in range(7):
            index = []
            data_value = []
            for i in range(len(data)-1):
                print(data[i][0], data[i][1], data[i+1][1][j])
                index.append(data[i][0])
                data_value.append((data[i][1], data[i+1][1][j]))
            all_data.append(data_value)
        return all_data

# if __name__ == '__main__':
#     load_data()

