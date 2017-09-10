# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-16

from MyCode import config
from MyCode.AutoTopicExtend import SimilarlyModel
from MyCode.AutoTopicExtend.SimilarlyModel import Config
from MyCode.tools import ReadFile


class WordClassify():
    """给定新词（原semantic_wordgroup.txt中不存在），确定词所属类别"""
    def __init__(self):
        _config = Config()
        self.Model = SimilarlyModel.getModel(_config)
        print self.Model

    def getWords(self):
        file = config.Semantic_dicPath+"semantic_wordgroup_new.txt"
        words = {}
        word_list = []
        sentences = ReadFile.readTXTFile(file)
        for sen in sentences:
            items = sen.strip().split(' ')
            if len(items) < 2:
                continue
            if words.has_key(items[1]):
                words[items[1]].append(items[0])
            else:
                words[items[1]] = [items[0]]
            word_list.append(items[0])
        return words,word_list

    def getClassOfWordByMinDistance(self,word,words_classed):
        min_distance = 0.0
        class_str = ""
        for key in words_classed.keys():
            words = words_classed[key]
            for w in words:
                try :
                    cur_distance = self.Model.similarity(unicode(w),unicode(word))
                except:
                    cur_distance = 0.0
                if cur_distance > min_distance:
                    min_distance = cur_distance
                    class_str = key
        return class_str

    def getNewWords(self):
        file = config.WordDicPath + "birds.txt"
        lines = ReadFile.readTXTFile(file)
        words = []
        for line in lines:
            words.extend(line.strip().split(" "))
        return words

    def wordClassify(self,words):
        words_classify = {}
        words_classed,word_list = self.getWords()
        print len(word_list)
        for word in words:
            if word not in word_list:
                words_classify[word] = self.getClassOfWordByMinDistance(word,words_classed)
        return words_classify