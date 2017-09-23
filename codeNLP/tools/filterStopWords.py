# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-31

import MyCode.config
import ReadFile


# 过滤标点符号和停用词
def filterStopWords(sentences,file=MyCode.config.StopWordPath+'stop_2.txt'):
    stopWords = ReadFile.readStopWord(file)
    filterSentences = []
    noFilterSentences = []
    for sentence in sentences:
        filter_words = []
        nofilterWords = []
        for sen in sentence:
            nofilterWords.append(sen)
            if sen not in stopWords:
                filter_words.append(sen)
        filterSentences.append(filter_words)
        noFilterSentences.append(nofilterWords)
    return filterSentences,noFilterSentences

def filterStopWordsInSentences(par_sentences):
    # file = "../../Data/StopWords/stop.txt"
    stopWords = ReadFile.readStopWord(MyCode.config.StopWordPath + 'stop_2.txt')
    filter_Par_Sentences = []
    for par_sentence in par_sentences:
        filterSentences = []
        for sen in par_sentence:
            words = []
            for word in sen:
                if word not in stopWords:
                    words.append(word)
            filterSentences.append(words)
        filter_Par_Sentences.append(filterSentences)
    return filter_Par_Sentences

def filterStopWords(Words):
    New_words = []
    stopWords = ReadFile.readStopWord(MyCode.config.StopWordPath + 'stop_2.txt')
    for word in Words:
        if word not in stopWords:
            New_words.append(word)
    return New_words

def filterStopWordFromSentences(sentences):
    stopWords = ReadFile.readStopWord(MyCode.config.StopWordPath + 'stop_2.txt')
    filter_sentences = []
    for sentence in sentences:
        filter_sentence = []
        for w in sentence:
            if w not in stopWords:
                filter_sentence.append(w)
        filter_sentences.append(filter_sentence)
    return filter_sentences



