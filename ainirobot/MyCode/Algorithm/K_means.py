# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-04

import sys
sys.path.append('..')
import random
from MyCode.ExtendWords import similarlyWord


class Cluster_K_means():
    '''
    ////该类使用K-means算法，解决话题关键词的相似词的聚类和获取类别下的相关的关键词////
    k_topic is cluster number
    distance = 1 not used
    repeats = 1 items
    normallise = Flase not used
    svd_dimensions to dimensionality reduction
    model need special ,default similarlyWord model
    model can be a class defined by yourself,must Implementation funcation self.similarly(value1,value2)
    '''
    def __init__(self,k_topic=20,distance=1, repeats=10,
                       conv_test=1e-6, initial_means=None,
                       normalise=False, svd_dimensions=None,
                       rng=None, avoid_empty_clusters=False,model=None):
        self.num_means = k_topic
        self.distance = distance
        self._max_difference = conv_test
        assert not initial_means or len(initial_means) == initial_means
        self._means = initial_means
        assert repeats >= 1
        assert not (initial_means and repeats > 1)
        self._repeats = repeats
        self._rng = (rng if rng else random.Random())
        self._avoid_empty_clusters = avoid_empty_clusters
        if model is None:
            self.model = similarlyWord.buildModel("wordRank_new_1")
        else:
            self.model = model

    # 计算所有词俩俩之间的距离
    # 返回距离辞典{(v1,v2):distance}
    def cal_Word_distance(self,values):
        words_num = len(values)
        word_dis = {}
        for i in xrange(values):
            for j in xrange(i,words_num):
                word_dis.setdefault((values[i],[values[j]]),self.model.similarly(values[i],values[j]))
        return word_dis

    # 聚类 迭代计算 生成聚类簇
    # 返回聚类簇的结果
    # 聚类 距离公式采用的是 —— 最大距离
    def Cluster(self,vector=None,tra=False,distanceType=False):
        if vector == None or len(vector) < self.num_means:
            return set(vector)
        self.clusters = []
        all_num = len(vector)
        items = 0
        distance = self.findMaxDistances
        if distanceType:
            distance = self.findMinDistance

        # init center
        # for i in xrange(self.num_means):
        #     self.clusters.append(set([vector[i]]))
        self.clusters = list(set(vector))
        self.result = None
        while items < self._repeats:
            change_num = 0
            newClusters = [list() for i  in xrange(self.num_means)]
            if self.result is None:
                self.result = [[self.clusters[i]] for i  in xrange(self.num_means)]
            for word in self.clusters:
                index,oldindex = distance(word)
                if index != oldindex:
                    change_num += 1
                # print newClusters,index
                newClusters[index].append(word)
            self.result = newClusters
            items += 1
            print("第%d次迭代！"%items)
        print("共迭代次数%d"%items)
        return self.result

    # 计算簇中的词与当前输入词的最大距离
    # 返回最大距离的簇的索引
    def findMaxDistances(self,word):
        min_distance = 0.0
        index = 0
        old_index = 0
        for i in xrange(self.num_means):
            for w in self.clusters[i]:
                try:
                    # print word,w
                    cur_distance = self.model.similarly(w,word)
                except :
                    cur_distance = 0
                finally:
                    if min_distance < cur_distance and cur_distance > 0:
                        min_distance = cur_distance
                        index = i
            i += 1
        return index,old_index

    def findMinDistance(self,value):
        min_distance = 100.0
        index = 0
        old_index = 0
        for i in xrange(self.num_means):
            for w in self.result[i]:
                try:
                    # print word,w
                    cur_distance = self.model.similarly(w, value)
                except:
                    cur_distance = 100
                finally:
                    if min_distance > cur_distance and cur_distance >= 0:
                        min_distance = cur_distance
                        index = i
            i += 1
        return index, old_index

def main():
    k_means = Cluster_K_means(k_topic=20,distance=None,repeats=1,conv_test=1e-6,initial_means=None,normalise=False,svd_dimensions=None,rng=None,avoid_empty_clusters=False)







