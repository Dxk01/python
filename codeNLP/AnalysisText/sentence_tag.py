# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-10

# today  i want to write my first code file in company

import nltk
import thulac
from  jieba import posseg

class Sentence_Tag():
    """
    句子标记
    """
    def __init__(self):
        self.thul = thulac.thulac()
        # self.jiebaPosseg = posseg

    #nltk 工具标记
    def tagSentence(self,sentence):
        words = nltk.word_tokenize(sentence)
        word_tag = nltk.pos_tag(words)
        return word_tag

    # 北京大学 thulac 标记
    def tagSentenceByThulac(self,sentence):
        sen = sentence.strip().replace(' ','')
        return self.thul.cut(sen,text=True)

    def tagSentenceByJieba(self,sentence):
        sen = sentence.strip().replace(" ",'')
        return posseg.cut(sen)

    def tagSentences(self,sentences,method=1):
        word_tag_sentences = []
        for sen in sentences:
            if method == 1:
                word_tag_sentences.append(self.tagSentence(sen))
            elif method == 2:
                word_tag_sentences.append(self.tagSentenceByThulac(sen))
            else:
                word_tag_sentences.append(self.tagSentenceByJieba(sen))
        return word_tag_sentences