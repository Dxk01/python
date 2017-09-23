#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
sys.path.append("../..")
reload(sys)


import codecs
import multiprocessing
import os
import time
import traceback

import jieba
import six
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

import MyCode.config
from MyCode.tools import ReadFile

sys.setdefaultencoding("utf-8")

class Config:
    data_path = MyCode.config.CorpusFilePath
    zhwiki_raw_t2s = 'corpus.txt'
    zhwiki_seg_t2s = 'souhu_fenci_no_filter'
    embedded_model_t2s = MyCode.config.ModelPath + 'wordRank_new_2_no_filter.model'
    embedded_vector_t2s = MyCode.config.ResultFilePath + "Vector_no_filter.model"
    stopWordPath = MyCode.config.StopWordPath


def dataprocess(_config):
    i = 0
    output = None
    if six.PY3:
        output = open(os.path.join(_config.data_path, _config.zhwiki_raw), 'w')
    else:
        output = codecs.open(os.path.join(_config.data_path, _config.zhwiki_raw), 'w')
    wiki = WikiCorpus(os.path.join(_config.data_path, _config.zhwiki_bz2), lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        if six.PY3:
            output.write(b' '.join(text).decode('utf-8', 'ignore') + '\n')
        else:
            output.write(' '.join(text) + '\n')
        i += 1
        if i % 10000 == 0:
            print('Saved ' + str(i) + ' articles')
    output.close()
    print('Finished Saved ' + str(i) + ' articles')

config = Config()
# dataprocess(config)

def is_alpha(tok):
    try:
        return tok.encode('ascii').isalpha()
    except UnicodeEncodeError:
        return False


def zhwiki_segment(_config,div_size=10 ,remove_alpha=True):
    i = 0
    files = []
    for i in xrange(div_size):
        files.append(codecs.open(os.path.join(_config.data_path, _config.zhwiki_seg_t2s+str("%02d.txt"%i)), 'w', encoding='utf-8'))
    print('Start...')
    stopWords = ReadFile.readStopWord(_config.stopWordPath + 'stop.txt')
    file_len = 0
    with codecs.open(os.path.join(_config.data_path, _config.zhwiki_raw_t2s), 'r', encoding='utf-8') as raw_input:
        # file_len = raw_input.
        line = raw_input.readline()
        while line:
            line = line.strip()
            i += 1
            if i % 100 == 0:
                print('line ' + str(i))
            # print(line)
            text = line.split()
            if True:
                text = [w for w in text if not is_alpha(w)]
            word_cut_seed = [jieba.cut(t) for t in text]
            tmp = ''
            for sent in word_cut_seed:
                for tok in sent:
                    if  tok in stopWords:
                        continue
                    tmp += tok + ' '
            tmp = tmp.strip()
            if tmp:
                try :
                    files[i%10].write(tmp + '\n')
                except:
                    print("file write error!")
                    continue
            line = raw_input.readline()
        for i in xrange(div_size):
            files[i].close()

# zhwiki_segment(config)


def word2vec(_config, saved=False):
    print('Start...')
    # read file
    sentences = []
    for i in xrange(10):
        file = os.path.join(_config.data_path, _config.zhwiki_seg_t2s + "{:02d}".format(i) + ".txt")
        sentences.extend(LineSentence(file))
    print("documents number :%d"%len(sentences))
    # model = Word2Vec(LineSentence(os.path.join(_config.data_path, _config.zhwiki_seg_t2s+"00.txt")),
    #                  size=50, window=5, min_count=5, workers=multiprocessing.cpu_count())
    model = Word2Vec(sentences,size=10,window=5,min_count=5,workers=multiprocessing.cpu_count()-2)
    if saved:
        print(_config.embedded_model_t2s)
        model.save(_config.embedded_model_t2s)
        model.wv.save_word2vec_format(_config.embedded_vector_t2s)
    print("Finished!")
    return model

def word2vecTrain(_config,saved=True):
    print('Start ...')
    model = word2vec(_config,saved=True)

    for i in xrange(1,10):
        file = os.path.join(_config.data_path, _config.zhwiki_seg_t2s+"{:02d}".format(i)+".txt")
        print(file)
        model.build_vocab(LineSentence(file))
        model.train(LineSentence(file))


def getModel(_config):
    print("Get model ... ...")
    model = None
    try :
        print(_config.embedded_model_t2s)
        model = Word2Vec.load(_config.embedded_model_t2s)
        return model
    except Exception ,e:
        print
        'str(Exception):\t', str(Exception)
        print
        'str(e):\t\t', str(e)
        print
        'repr(e):\t', repr(e)
        print
        'e.message:\t', e.message
        print
        'traceback.print_exc():';
        traceback.print_exc()
        print
        'traceback.format_exc():\n%s' % traceback.format_exc()
        start = time.time()
        model = word2vec(_config,saved=True)
        end = time.time()
    return model


def wordsimilarity(word, model):
    semi = ''
    try:
        semi = model.most_similar(word, topn=10)
    except KeyError:
        print('The word not in vocabulary!')
    for term in semi:
        print('%s,%s' % (term[0], term[1]))

#

def wordToWordSimilarly(word1,word2,model):
    semi = 0.0
    try:
        semi = model.similarity(word1,word2)
    except KeyError:
        # print('%s %sThe word not in vocabulary!'%(word1,word2))
        print(semi)
    return semi



# word2vecTrain(config,True)

# model = word2vec(config, saved=True)
# model = getModel(config)
# print(model)
# wordsimilarity(word=u"爸爸妈妈",model=model)
# print("%s和%s的相似度是：%lf"%("爸爸","妈妈",wordToWordSimilarly(word1=u"爸爸",word2=u"妈妈",model=model)))