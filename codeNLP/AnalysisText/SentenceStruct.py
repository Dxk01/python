# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-10

import Levenshtein as Ls

class SentenceStruct():
    """
    句式
    """
    def __init__(self):
        pass

    # 输入数据预处理
    def preProcess(self,sentences):
        sentences_word_tag = []

        for sen in sentences:
            words_tag = sen.split(" ")
            word_sentence = []
            for word in words_tag:
                items = word.split("_")
                if len(items) != 2:
                    continue
                word_sentence.append((items[0],items[1]))
            sentences_word_tag.append(word_sentence)

        return sentences_word_tag

    # 句式分类根据词标注
    """
        相同标记序列的句子即视为相同句式
    """
    def SimiSentenceStruct(self,sentences):
        sentences_word_tag = self.preProcess(sentences)
        sentences_class_list = None

        for sentence  in sentences_word_tag:
            index = self.cal_simiValue(sentence,sentences_class_list)
            if index >= 0:
                sentences_class_list[index].append(sentence)
            else:
                if sentences_class_list:
                    sentences_class_list.append([sentence,])
                else:
                    sentences_class_list = [[sentence,]]

        return sentences_class_list

    # 计算句子的相似类别，如果没有相似句型返回-1，否则返回类别索引
    def cal_simiValue(self,sen,sentences_class_list):
        if sentences_class_list == None:
            return -1
        i = 0
        for sentences_class in sentences_class_list:
            j = 0
            if len(sen) != len(sentences_class[0]):
                i += 1
                continue
            while j < len(sen) and sen[j][1] == sentences_class[0][j][1]:
                j += 1
            if j == len(sen):
                return i
            i += 1
        return -1

    """
        根据相同句式，进一步归纳句式结构
    """
    def SentenceStructExtract(self,sentence_class_list):
        sentences = {}
        # 初始化过滤集合
        unfilterSet = ['v','u','m','q','d']
        for sentence_class in sentence_class_list:
            for sentence in sentence_class:
                if len(sentence) <=3:
                    break
                re_sen = ''
                for word in sentence:
                    if word[1] not in unfilterSet:
                        re_sen += word[1]
                    else:
                        re_sen += word[0]
                if sentences.has_key(re_sen):
                    num = sentences.get(re_sen) + 1
                    sentences.pop(re_sen)
                    sentences.setdefault(re_sen,num)
                else :
                    sentences.setdefault(re_sen,1)

        return sentences

    def SentenceStructExtractTem(self,sentences):
        tem_clusters = None
        for sen in sentences:
            if tem_clusters == None:
                tem_clusters = [[sen]]
                continue
            index = self.cal_Levenshtein_distance(sen,tem_clusters)
            if index < 0:
                tem_clusters.append([sen])
                continue
            else:
                tem_clusters[index].append(sen)

        return tem_clusters

    def cal_Levenshtein_distance(self,str_sen,tem_clusters):
        index = -1
        distance_min = 20
        for i in xrange(len(tem_clusters)):
            for sen in enumerate(tem_clusters[i]):
                # print sen[1],str_sen
                cur_distance = Ls.distance(sen[1],str_sen)
                if distance_min > cur_distance and cur_distance <= 4 and cur_distance > 0:
                    distance_min = cur_distance
                    print sen[1],str_sen
                    index = i

        return index

# def main():
    # SS = SentenceStruct()
    # SS.cal_Levenshtein_distance()


