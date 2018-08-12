# encodig=utf-8
# Writer : lgy
# dateTime : 2018-07-27

from preprocess import loaddata
import pickle as pkl
import numpy as np
import tensorflow as tf
from sklearn import random_projection
import random

output_path_dir = "Data/static"


def getApipv(file="Data/SourceData/train.csv"):
    data_iter = loaddata(file)
    # lines = next(data_iter)
    api_static_result = {}
    return_result_static = {}
    api_id = {}
    return_id = {}
    api_index = 1
    return_index = 1
    for lines in data_iter:
        print(lines[0])
        for line in lines:
            feature_name = str(line[0] + "_" + line[2])
            if feature_name in api_static_result:
                api_static_result[feature_name] += 1
            else:
                api_static_result[feature_name] = 1

            api_name = str(line[2])
            if api_name not in api_id:
                api_index = api_index + 1
                api_id[api_name] = api_index

            return_result = str(line[-2])
            if return_result not in return_id:
                return_id[return_result] = return_index
                return_index += 1

            feature_name_2 = str(line[0] + "_" + line[-2])
            if feature_name_2 in return_result_static:
                return_result_static[feature_name_2] += 1
            else:
                return_result_static[feature_name_2] = 1
        # lines = next(data_iter)
        # break
    return api_static_result, return_result_static, api_id, return_id


# api_static, return_static, api_idMap, return_idMap = getApipv("Data/SourceData/test.csv")
#
# with open(output_path_dir+"/test_api_static.pkl", "wb") as api_file:
#     print(len(api_static))
#     pkl.dump(api_static, api_file)
# #
# with open(output_path_dir+"/test_return_static.pkl", "wb") as return_file:
#     print(len(return_static))
#     pkl.dump(return_static, return_file)
# #
# with open(output_path_dir+"/test_api_idmap.pkl", "wb") as api_idmap_file:
#     print(len(api_idMap))
#     pkl.dump(api_idMap, api_idmap_file)
#
# with open(output_path_dir+"/test_return_idMap.pkl", "wb") as return_idMap_file:
#     print(len(return_idMap))
#     pkl.dump(return_idMap, return_idMap_file)

def getStaticfeature(input_dir="Data/SourceData", output_dir=output_path_dir, train=True):
    file = input_dir + "/train.csv"
    if not train:
        file = input_dir + "/test.csv"
    data_iter = loaddata(file)
    api_static = None
    return_static = {}
    api_index = 0
    return_index = 0
    api_map = {}
    return_map = {}
    filename = output_dir + "/static_feature.txt"
    if not train:
        filename = output_dir + "/test_static_feature.txt"
    fp = open(filename, "w")
    for lines in data_iter:

        for line in lines:
            api_feature = str(line[0] + "_api_" + line[2])
            if api_static and api_feature in api_static:
                api_static[api_feature] += 1
            elif api_static and api_feature not in api_static:
                for key in api_static:
                    fp.write(key + "\t" + str(api_static[key]) + "\n")
                api_static = {api_feature: 1}
            else:
                api_static = {api_feature: 1}
            apiName = str(line[2])
            if apiName not in api_map:
                api_index += 1
                api_map[apiName] = api_index

            return_feature = str(line[0] + "_return_" + line[-2])
            if return_static and return_feature in return_static:
                return_static[return_feature] += 1
            elif return_static and return_feature not in return_static:
                for key in return_static:
                    fp.write(key + "\t" + str(return_static[key]) + "\n")
                return_static = {return_feature: 1}
            else:
                return_static = {return_feature: 1}
            returnValue = str(line[-1])
            if returnValue not in return_map:
                return_index += 1
                return_map[returnValue] = return_index
    fp.close()
    return api_map, return_map


def getStaticfeatureExample(input_dir="Data/SourceData", output_dir=output_path_dir):
    file = input_dir + "/test.csv"
    data_iter = loaddata(file)
    api_static = None
    return_static = {}
    api_index = 0
    return_index = 0
    api_map = {}
    return_map = {}
    filename = output_dir + "/test_static_feature.txt"
    fp = open(filename, "w")
    for lines in data_iter:

        for line in lines:
            api_feature = str(line[0] + "_api_" + line[1])
            if api_static and api_feature in api_static:
                api_static[api_feature] += 1
            elif api_static and api_feature not in api_static:
                for key in api_static:
                    fp.write(key + "\t" + str(api_static[key]) + "\n")
                api_static = {api_feature: 1}
            else:
                api_static = {api_feature: 1}
            apiName = str(line[1])
            if apiName not in api_map:
                api_index += 1
                api_map[apiName] = api_index

            return_feature = str(line[0] + "_return_" + line[-2])
            if return_static and return_feature in return_static:
                return_static[return_feature] += 1
            elif return_static and return_feature not in return_static:
                for key in return_static:
                    fp.write(key + "\t" + str(return_static[key]) + "\n")
                return_static = {return_feature: 1}
            else:
                return_static = {return_feature: 1}
            returnValue = str(line[-1])
            if returnValue not in return_map:
                return_index += 1
                return_map[returnValue] = return_index
    fp.close()
    return api_map, return_map


# apiMap, returnMap = getStaticfeature()
# #
# with open(output_path_dir+"/api_idmap.pkl", "wb") as api_idmap_file:
#     print(len(apiMap))
#     pkl.dump(apiMap, api_idmap_file)
#
# with open(output_path_dir+"/return_idMap.pkl", "wb") as return_idMap_file:
#     print(len(returnMap))
#     pkl.dump(returnMap, return_idMap_file)
#
#
# test_apiMap, test_returnMap = getStaticfeatureExample()
# # #
# with open(output_path_dir+"/test_api_idmap.pkl", "wb") as api_idmap_file:
#     print(len(test_apiMap))
#     pkl.dump(test_apiMap, api_idmap_file)
#
# with open(output_path_dir+"/test_return_idMap.pkl", "wb") as return_idMap_file:
#     print(len(test_returnMap))
#     pkl.dump(test_returnMap, return_idMap_file)

def combineFeature(input="Data/static", output="Data/static", train=True):
    input_file = input + "/static_feature.txt"
    output_file = output + "/combine_static_feature.txt"
    if not train:
        output_file = output + "/test_combine_static_feature.txt"
        input_file = input + "/test_static_feature.txt"
    feature_dic = {}
    with open(input_file, "r") as fr:
        line = fr.readline()

        while line:
            term = line.strip().split("\t")
            featureName = term[0]
            value = int(term[1])
            if featureName in feature_dic:
                feature_dic[featureName] += value
            else:
                feature_dic[featureName] = value
            line = fr.readline()

    with open(output_file, "w") as fp:
        print(len(feature_dic))
        for key in feature_dic:
            fp.write(key + "\t" + str(feature_dic[key]) + "\n")


# combineFeature()

# combineFeature(train=False)

def getDense(input_dir="Data/static", train=True, batch_size=64):
    api_mapfile = input_dir + "/api_idmap.pkl"
    return_mapfile = input_dir + "/return_idMap.pkl"
    file = input_dir + "/combine_static_feature.txt"
    if not train:
        # api_mapfile = input_dir+"/test_api_idmap.pkl"
        # return_mapfile = input_dir+"/test_return_idMap.pkl"
        file = input_dir + "/test_combine_static_feature.txt"
    api_dic = None
    with open(api_mapfile, "rb") as fp:
        api_dic = pkl.load(fp)

    return_dic = None
    with open(return_mapfile, "rb") as fp:
        return_dic = pkl.load(fp)

    api_size = len(api_dic) + 1
    return_size = len(return_dic) + 1

    print("api_feature size:", api_size, "return feature size:", return_size)

    api_feature_dic = {}
    return_feature_dic = {}
    with open(file, "r") as fp:
        lines = fp.readlines(1)
        while lines:
            for line in lines:
                term = line.strip().split("\t")
                featureG = term[0].split("_")
                featureValue = int(term[1])
                imei = featureG[0]
                featureType = featureG[1]
                featureName = featureG[2]
                if featureType == "api":
                    index = 0
                    if featureName in api_dic:
                        index = int(api_dic[featureName])

                    if imei in api_feature_dic:
                        api_feature_dic[imei][index] += featureValue
                    else:
                        api_feature_dic[imei] = np.zeros([api_size])
                        api_feature_dic[imei][index] = featureValue

                if featureType == "return":
                    index = 0
                    if featureName in return_dic:
                        index = int(return_dic[featureName])

                    if imei in return_feature_dic:
                        return_feature_dic[imei][index] += featureValue
                    else:
                        return_feature_dic[imei] = np.zeros([return_size])
                        return_feature_dic[imei][index] = featureValue
            lines = fp.readlines(1)

    dense = {}
    i = 0
    for key in api_feature_dic:
        api_vector = api_feature_dic[key]  # .reshape([1, api_size])
        return_vector = return_feature_dic[key]  # .reshape([1, return_size])

        dense[key] = np.concatenate((api_vector, return_vector), 0)
        # tf.concat([api_vector, return_vector], 1)[0]
        # if i % 1000 == 0:
        #     print(api_vector)
        #     print(return_vector)
        #     print(dense[key])
        # i += 1
        # if i >= 10000:
        #     break
    return dense


def getLabel(input_dir="Data/SourceData", output_dir="Data/static", train=True):
    input_file = input_dir + "/train.csv"
    output_file = output_dir + "/label.txt"
    if not train:
        return None
    data_iter = loaddata(input_file)
    data_lab = {}
    with open(output_file, "w") as fp:
        for lines in data_iter:
            for line in lines:
                if line[0] not in data_lab:
                    data_lab[line[0]] = line[1]
                    fp.write(line[0] + "\t" + line[1] + "\n")
    return data_lab


def getLabel_pre(file="Data/static/label.txt"):
    labels = {}
    with open(file, "r") as fp:
        line = fp.readline()
        while line:
            term = line.strip().split("\t")
            imei = term[0]
            label = term[1]
            if imei not in labels:
                labels[imei] = label
            line = fp.readline()
    return labels


data_lab = getLabel_pre()
print(len(data_lab))
dense_data = getDense()
print("train data size:", len(dense_data))

predict_data = getDense(train=False)
print("test data size:", len(predict_data))


def getExampleTrain(dense, labs, pro=0.1):
    train_data = []
    for key in dense:
        lab = labs[key]
        example = dense[key]
        train_data.append([example, lab])
    # train_datrain_data)
    train_X = []
    train_Y = []
    test_X = []
    test_Y = []
    for line in train_data:
        proboli = random.random()
        if proboli > pro:
            train_X.append(line[0])
            train_Y.append(line[1])
        else:
            test_X.append(line[0])
            test_Y.append(line[1])
    return train_X, train_Y, test_X, test_Y


def getExampleTest(dense):
    test_data = []
    for key in dense:
        example = dense[key]
        test_data.append(example)
    return test_data


import math


def log_loss(pre_labs, true_labs):
    real_dataSize = len(true_labs)
    pre_dataSize = len(pre_labs)
    if real_dataSize != pre_dataSize:
        return 0.0
    loss = 0.0
    for i in range(real_dataSize):
        for index in range(6):
            if int(true_labs[i]) == 1.0:
                if pre_labs[i][index] <= 0.0:
                    loss += math.log10(0.000001)
                else:
                    loss += math.log10(pre_labs[i][index])
            else:
                if pre_labs[i][index] >= 1.0:
                    loss += math.log10(0.000001)
                else:
                    loss += math.log10(1.0 - pre_labs[i][index])

    return - (loss / real_dataSize)


train_X, train_Y, test_X, test_Y = getExampleTrain(dense_data, data_lab, 0.1)

# _, _, test_X, test_Y = getExampleTrain(dense_data, data_lab, 0.1)
vector_size = len(train_X[0])
print("train data length:", len(train_X[0]))

pre_data = getExampleTest(predict_data)

print("test data length:", len(pre_data[0]))

from sklearn import random_projection
from sklearn import preprocessing

# transformer = random_projection.GaussianRandomProjection()
# train_X =  np# train_X)
# test_X = transformer.transform(test_X)

# enc = preprocessing
# train_Y = enc.fit_transform(train_Y)
# test_Y = enc.transform(test_Y)

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

# clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(32, 64, 128, 64, 32), learning_rate="adaptive",
#                     activation="relu", learning_rate_init=0.0001, verbose=1)
# clf = DecisionTreeClassifier(class_weight="balanced")
# clf = LogisticRegression(class_weight=None, n_jobs=3, tol=0.0001,
#                          fit_intercept=True, verbose=1)
# clf.fit(train_X, train_Y)
import tensorflow as tf
from tflearn.models.dnn import DNN
# from tflearn.models.dnn import
import tflearn
from sklearn.preprocessing import OneHotEncoder

one_hot = OneHotEncoder(sparse=False)
# .fit(train_Y)
train_Y = one_hot.fit_transform(np.reshape(train_Y, (-1, 1)))
test_Y = one_hot.transform(np.reshape(test_Y, (-1, 1)))
print(train_Y)
lab_size = len(train_Y[0])
# Building deep neural network
# X = tf.placeholder(shape=(None, vector_size), dtype=tf.float32)
# Y = tf.placeholder(shape=(None, lab_size), dtype=tf.float32)

drop_pro = 0.8

input_layer = tflearn.input_data(shape=[None, vector_size])
dense1 = tflearn.fully_connected(input_layer, 64, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)
dropout1 = tflearn.dropout(dense1, drop_pro)
dense2 = tflearn.fully_connected(dropout1, 128, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)
dropout2 = tflearn.dropout(dense2, drop_pro)
dense3 = tflearn.fully_connected(dropout1, 64, activation='tanh',
                                 regularizer='L2', weight_decay=0.001)
dropout3 = tflearn.dropout(dense2, drop_pro)
softmax = tflearn.fully_connected(dropout3, lab_size, activation='softmax')

# Regression using SGD with learning rate decay and Top-3 accuracy
sgd = tflearn.SGD(learning_rate=0.01, lr_decay=0.96, decay_step=1000)
adam = tflearn.Adam(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08, use_locking=False, name="Adam")
# loss = tflearn.losses.L2()
# top_k = tflearn.metrics.Top_k(6)
accu  = tflearn.metrics.Accuracy()
net = tflearn.regression(softmax, optimizer=adam, metric=accu)
# optimizer = tflearn.optimizers.Optimizer(learning_rate=0.01, False, "")
# loss = tf.reduce_mean(tf.nn.log_poisson_loss(logits=softmax, labels=Y))
# optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(loss)
# init = tf.global_variables_initializer()


dnn = DNN(net, clip_gradients=5.0, tensorboard_verbose=0,
          tensorboard_dir='/tmp/tflearn_logs/', checkpoint_path=None,
          best_checkpoint_path=None, max_checkpoints=None,
          session=None, best_val_accuracy=0.0)

dnn.fit(train_X, train_Y, 10, validation_set=(test_X, test_Y),
        show_metric=True, run_id="dense_model")

pre_Y = dnn.predict(test_X)
# pre_pro_Y = dnn.predict_proba(test_X)


# pre_Y = clf.predict(test_X)
# pre_pro_Y = clf.predict_proba(test_X)
#
# def accurcy(test_Y, pre_Y):
#     print(len(pre_Y), len(test_Y))
#     all_size = len(test_X)
#     right = 0
#     pre_not0 = 0
#     test_not0 = 0
#     for i in range(all_size):
#         if test_Y[i] == pre_Y[i]:
#             right += 1
#         if pre_Y[i] != "0":
#             pre_not0 += 1
#         if test_Y[i] != '0':
#             test_not0 += 1
#     print("accurcy:" + str(float(right) / all_size))


# accurcy(test_Y, pre_Y)
# dnn.evaluate(X=test_X, Y=test_Y, batch_size=128)
#
# print("log loss:", log_loss(test_Y, pre_pro_Y))
# accu = tflearn.metrics.accuracy()
# accu.build(softmax, test_Y, pre_Y)
# accu.get_tensor()
# name = "MLPClassifier"
# name = "DecisionTreeClassifier"
# with open("model/model_" + name + ".ml", "wb") as fp:
#     pkl.dump(clf, fp)

# model = None
# with open("model/model_" + name + ".ml", "rb") as fp:
#     model = pkl.load(fp)

# result = clf.predict_proba(pre_data)
result = dnn.predict(pre_data)

import pandas as pd

dataF = pd.DataFrame(result)

dataF.to_csv("Data/result/3rd_security_submit.csv", ",")
