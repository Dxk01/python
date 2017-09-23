# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-22
import sys
sys.path.append(".")
reload(sys)
from MyCode import config
from MyCode.tools import ReadFile
import logging
from collections import OrderedDict
import jieba
# lo

class Word(object):
    def __init__(self,word):
        self.text = word
        self.word_semantic = None
        self.word_semantic_tokens = None

    def buildWord(self,text=u"成都"):
        self.text = text

class Sentence(object):
    def __init__(self):
        self.ss = None
        self.text = None
        self.text_type = None
        self.words = None

    def buildSentence(self,text="成都好听嘛"):
        self.text = text
        # print self.text
        ws = jieba.cut(text)
        sen_words = []
        # self.words =
        for w in ws:
            word = Word(w)
            # word.buildWord(w)
            sen_words.append(word)
        self.words = sen_words

class MulSemanticDic(object):
    """ Class if identify multi Emotion"""

    def __init__(self):
        self.mul_word_dic = None
        self.semantic_index = None

        return

    # 提取 多语义词
    def getMulSemanticWord(self,file = config.WordDicPath+"semantic_wordgroup_new.txt"):
        # with open(file,'r') as fp:
        # word_sentences = ReadFile.readTXTFile(file)
        word_dic = {}
        mul_word_dic = {}
        with open(file,'r') as fp:
            for line in fp:
                iterms = line.strip().split(" ")
                if len(iterms) != 2:
                    continue
                if word_dic.has_key(iterms[0]):
                    if mul_word_dic.has_key(iterms[0]):
                        mul_word_dic[iterms[0]].append(iterms[1])
                    else:
                        mul_word_dic[iterms[0]] = [word_dic[iterms[0]],iterms[1]]
                else:
                    word_dic[iterms[0]] = iterms[1]
        self.mul_word_dic = mul_word_dic
        return mul_word_dic

    # 加载 多语意 辞典
    def loadDic(self,modelConfig=config):
        logging.info("call multip semantic dic load")
        mul_word_dic = {}
        with open(modelConfig.WordDicPath+"MulSemantic_wordgroup.txt",'r') as fp:
            for line in fp:
                iterms = line.strip().split(" ")
                if len(iterms) < 2:
                    continue
                if mul_word_dic.has_key(unicode(iterms[0])):
                    mul_word_dic[unicode(iterms[0])][unicode(iterms[2])] = iterms[1]
                else:
                    mul_word_dic[unicode(iterms[0])] = {unicode(iterms[2]):iterms[1]}
        self.mul_word_dic = mul_word_dic

    # 判别句子中的
    def tagSemantic(self,sentence):
        length = len(sentence.words)
        words = sentence.words
        word_text_list = []
        for w in sentence.words:
            word_text_list.append(w.text)

        for i in xrange(length):
            # print self.mul_word_dic.keys()
            if words[i].text in self.mul_word_dic.keys():
                for key in self.mul_word_dic[words[i].text]:
                    pattern_words = set(key.split("|"))
                    if set(word_text_list) & set(key.split("|")):
                        words[i].word_semantic = self.mul_word_dic[words[i].text].get(key)
                        words[i].word_semantic_tokens = words[i].word_semantic.split("|")
                if words[i].word_semantic == None:
                    words[i].word_semantic = self.mul_word_dic[words[i].text].get("1")
                    words[i].word_semantic_tokens = words[i].word_semantic.split("|")

        return


    #
# filter semantic word
def filter(file = config.WordDicPath+"semantic_wordgroup_new.txt"):
    word_sentences = ReadFile.readTXTFile(file)
    word_dic = {}
    for word in word_sentences:
        iterms = word.strip().split(" ")
        if len(iterms) != 2:
            continue
        if iterms[0] in word_dic:
            if iterms[1] not in word_dic[iterms[0]] :
                word_dic[iterms[0]].append(iterms[1])
        else:
            word_dic[iterms[0]] = [iterms[1]]
    return word_dic

# /Users/orion/miniconda2/envs/chat/lib/python2.7/collections.py

# 写结果到文件
def WriteResultToFile(mul_word_dic,file = config.WordDicPath+"MulSemantic_wordgroup.txt"):
    with open(file,"w") as fp:
        for key in mul_word_dic.keys():
            iterms = mul_word_dic[key]
            if len(iterms) < 2:
                continue
                # print key
            i = 1

            for iterm in iterms:
                fp.write(key+u" "+iterm+u" "+str(i)+u"\n")
                i+=1


def main():
    # word_dic = filter()
    # WriteResultToFile(word_dic,file= config.WordDicPath+"semantic_wordgroup_new.txt")
    # mul_word_dic = getMulSemanticWord()

    # WriteResultToFile(mul_word_dic)
    sentence = Sentence()
    sentence.buildSentence("成都好听吗")
    Ms = MulSemanticDic()
    # Ms.getMulSemanticWord()
    # mul_word_dic = Ms.getMulSemanticWord()
    # WriteResultToFile(mul_word_dic)
    Ms.loadDic()
    Ms.tagSemantic(sentence)
    for w in sentence.words:
        print w.word_semantic

if __name__ == "__main__":
    main()



