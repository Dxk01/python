# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-16

from MyCode import config
from MyCode.Algorithm import K_means
from MyCode.AutoTopicExtend import SimilarlyModel
from MyCode.AutoTopicExtend.SimilarlyModel import Config
from MyCode.tools import ReadFile


class ClassRefine():
    def __init__(self):
        _config = Config()
        self.model = SimilarlyModel.getModel(_config)

    def getWords(self):
        file = config.Semantic_dicPath+"semantic_wordgroup_new.txt"
        words = {}
        sentences = ReadFile.readTXTFile(file)
        for sen in sentences:
            items = sen.strip().split(' ')
            if len(items) < 2:
                continue
            if words.has_key(items[1]):
                words[items[1]].append(items[0])
            else:
                words[items[1]] = [items[0]]
        return words

    def ClassifyWord(self,words):
        k_means = K_means.Cluster_K_means(k_topic=20, distance=None, repeats=1, conv_test=1e-6, initial_means=None,
                                  normalise=False, svd_dimensions=None, rng=None, avoid_empty_clusters=False)
        clusters_set = {}
        for key in words.keys():
            keyWords = words[key]
            clusters = k_means.Cluster(keyWords)
            clusters_set[key] = clusters
        return clusters_set
