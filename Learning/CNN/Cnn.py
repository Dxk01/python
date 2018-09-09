# _*_ coding:utf8 _*_
'''
Pedagogical example realization of seq2seq recurrent neural networks, using TensorFlow and TFLearn.
More info at https://github.com/ichuang/tflearn_seq2seq
'''

# from __future__ import division, print_function

import sys
# sys.setdefaultencoding('utf-8')

import tensorflow as tf
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression
from tflearn.data_utils import to_categorical, pad_sequences
# from tflearn.datasets import imdb
import pickle
import numpy as np
import random

# import


def load_data(file="data\data.txt"):
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
    # print(len(data))
    for j in range(7):
        data_value = []
        for i in range(len(data) - 1):
            # print(data[i][0], data[i][1], data[i + 1][1][j])
            linedata = []
            for v in data[i][1]:
                linedata.append(v)
            linedata.append(data[i + 1][1][j])
            data_value.append(linedata)
        all_data.append(data_value)
    return all_data


def random_shuffle(data_a, pro_h=0.1):
    # data_array = np.array(data)
    # data_array = np.random.sample(data_a)
    train_X = []
    train_Y = []
    test_X = []
    test_Y = []
    pro = 0.0
    for v in data_a:
        pro = random.uniform(0, 1)
        if pro < pro_h:
            test_X.append(v[:-1])
            test_Y.append(v[-1])
        else:
            train_X.append(v[:-1])
            train_Y.append(v[-1])
    return train_X, train_Y, test_X, test_Y


"""
还是加载imdb.pkl数据
"""
data = load_data()
train_d = data[0]
# train_data = np.
train_x, train_y, test_x, test_y = random_shuffle(train_d)

"""
转化为固定长度的向量，这里固定长度为100
"""
trainX = pad_sequences(train_x, maxlen=7, value=0.)
testX = pad_sequences(test_x, maxlen=7, value=0.)
"""
二值化向量
"""
trainY = to_categorical(train_y, nb_classes=10)
testY = to_categorical(test_y, nb_classes=10)
"""
构建卷积神经网络，这里卷积神经网网络为1d卷积
"""
network = input_data(shape=[None, 7], name='input')
print(network)
network = tflearn.embedding(network, input_dim=10, output_dim=512)
# print(network.train_one_sample())
# merge_data = []
# for i in range(32):
#     branch = conv_1d(network, 1024, i+3, padding='valid', activation='relu', regularizer="L2")
#     merge_data.append(branch)
branch2 = conv_1d(network, 512, 4, padding='valid', activation='relu', regularizer="L2")
branch3 = conv_1d(network, 512, 5, padding='valid', activation='relu', regularizer="L2")
branch1 = conv_1d(network, 512, 3, padding='valid', activation='relu', regularizer="L2")
# branch4 = conv_1d(network, 512, 6, padding='valid', activation='relu', regularizer="L2")
# branch5 = conv_1d(network, 512, 7, padding='valid', activation='relu', regularizer="L2")
# branch6 = conv_1d(network, 512, 1, padding='valid', activation='relu', regularizer="L2")
# branch7 = conv_1d(network, 512, 2, padding='valid', activation='relu', regularizer="L2")
# branch8 = conv_1d(network, 512, 10, padding='valid', activation='relu', regularizer="L2")
network = merge([branch1, branch2, branch3], mode='concat', axis=1)
print(network)
network = tf.expand_dims(network, 2)
print(network)
network = global_max_pool(network)
network = dropout(network, 0.5)
print(network)
network = fully_connected(network, 10, activation='softmax')
network = regression(network, optimizer='adam', learning_rate=0.001,
                     loss='categorical_crossentropy', name='target')
"""
训练开始
"""
model = tflearn.DNN(network, tensorboard_verbose=3)
model.fit(trainX, trainY, n_epoch=200, shuffle=True, validation_set=(testX, testY), show_metric=True, batch_size=32)
"""
模型保存
"""
model.save("log\cnn.model")
"""
做测试使用
"""
# print(model.evaluate(testX, testY, batch_size=32))
test = np.random.randint(0, 10, size=7).reshape(1, 7)
print(test)
print("测试结果：", model.predict_label(test))
