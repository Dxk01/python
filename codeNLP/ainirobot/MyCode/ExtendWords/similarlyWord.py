# _*_ coding: UTF-8 _*_
# writer : lgy
# data : 2017-07-24

# today  i want to write my first code file in company

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import  jieba.analyse
from gensim.models import word2vec
import math
from MyCode.tools import Participle, filterStopWords, ReadFile
import MyCode.config
# from pattern import tokenize
from nltk import tokenize

class TextIter(object):
    def __init__(self):
        self.file = MyCode.config.CorpusFilePath + 'souhu_fenci.txt'

    def __iter__(self):
        with open(self.file,'r') as fp:
            line = fp.readline()
            while line :
                if line != '':
                    tockenLine = ''.join(tokenize(line))
                    word_sentences = [word for word in tockenLine.split()]
                    yield word_sentences

#  输出词
def output(sentences):
    for sentence in sentences:
        for sen in sentence:
            print sen,
        print
#  对比输出
def outputCom(preSentences,newSentences):
    if len(preSentences) != len(newSentences):
        return
    for i in xrange(len(preSentences)):
        print '第%s句：'%i
        line = preSentences[i]
        for sen in line:
            print sen,
        print ''
        # print newSentences[i]
        for sen in newSentences[i]:
            print sen,
        print ''

# 读取目录下所有文件的问句,并分词
def getFileContext_Participle(dirPath=MyCode.config.CorpusFilePath):
    # files = ReadFile.getAllFilesInDir(dirPath)
    # sentences = ReadFile.getAllFilesContext(files,dirPath)
    #for test
    sentences = ReadFile.readTXTFile(dirPath + 'corpus.txt')
    par_sentences = Participle.Participle(sentences[:10])
    par_filter_sentences = filterStopWords.filterStopWords(par_sentences)
    # return wordTostr(par_filter_sentences)
    return par_filter_sentences

# 读取文件
def getFileSentence():
    filepath = "../Data/corpus/"
    files = ['favor0721.xlsx','inter0721.xlsx','Sentence_QR_pair_0714.xlsx']
    sentences = []
    for file in files:
        Q,R = ReadFile.getFileSentence(filepath + file)
        sentences.extend(Q)
    return sentences
#
def getTxtFileSentence():
    file = "../Result/corpus.txt"
    # sentences = ReadFile.readTXTFile(file)
    fr = open(file,'r')
    # ket_sentences = Participle.Participle(sentences)
    i = 0
    with open("../Result/souhu_fenci.txt","w") as fp:
        line = fr.readline()
        while line:
            sen = jieba.cut(line)
            write_line = ''
            for w in sen:
                write_line += w + ' '
            fp.write(write_line+"\n")
            line = fr.readline()
            if i %1000 == 0:
                 print i
            i += 1
    fr.close()

# 关键词提取
def extractKeyWord(sentences,topn = 3):
    length = len(sentences)
    print "分析句子",length,"个"
    tag_sentences = []
    for i in xrange(length):
        tag_sentences.append(jieba.analyse.extract_tags(sentences[i]))
    return tag_sentences

# 词 成 串
def sentence_word(tag_sentences):
    sentences = []
    for sentence in tag_sentences:
        sentence = ''
        for word in sentence:
            sentence += word + ' '
        sentences.append(sentence)
    return sentences

# 串 转 词
def strToWord(sentences):
    word_sentences = []
    for sen in sentences:
        words = sen.split()
        word_sentences.append(words)
    return word_sentences

# 词 转 串
def wordTostr(par_word_sentences):
    sentences = []
    for par_word_sentence in par_word_sentences:
        line = ''
        for par_word in par_word_sentence:
            line += par_word + ' '
        print line
        sentences.append(line)
    return sentences

def cal_similrity_model(sentences):
    model = word2vec.Word2Vec(sentences,workers=8)
    return model

class TextLoader(object):
    def __init__(self,tag_sentences):
        self.tag_sentences = tag_sentences

    def __iter__(self):
        for sentence in self.tag_sentences:
            sentence = ''
            for word in sentence:
                sentence += word + ' '
            yield sentence

def similarity_Word(model,words):
    with open("../Result/similary_Word.txt",'w') as fp:
        for word in words:
           try:
               simi_words = model.most_similar(str(word))
               fp.write(word+"的相似词有：\n")
               print word,"的相似词有"
               for si_word in simi_words:
                   print '\t',si_word[0],":",si_word[1]
                   fp.write('\t'+si_word[0]+":"+str(si_word[1])+'\n')
           except KeyError:
               print KeyError
               print word
               continue

def similarly(model,word1,word2):
    try :
        sim = model.similarity(word1,word2)
    except :
        print 1
        sim = 0
    return sim

def buildModel(Name = "wordRank_filter"):
    file = MyCode.config.ModelPath + Name + '.model'
    model = None
    try:
        model = word2vec.Word2Vec.load(file)
    except :
        # word_sentences = getFileContext_Participle()
        # sentences = wordTostr(word_sentences)
        # sentences = TextIter()TextIter
        sentences = ReadFile.readTXTFile(MyCode.config.CorpusFilePath + 'souhu_fenci.txt')
        model = word2vec.Word2Vec(sentences[:10],min_count=1,workers=8)
        model.save(file)
    return model


def analysisSimilary_Word(model, file=MyCode.config.CorpusFilePath + "favor0721.xlsx", sheet='节日210'):
    sentences,R_S = ReadFile.getOneSheetContext(file, sheet)
    cla_Key_words = []
    for sentence in sentences:
        # print sentence
        key_sentence = jieba.analyse.extract_tags(sentence)
        for w in key_sentence:
            cla_Key_words.append(w)
    cla_Key_words = list(set(cla_Key_words))
    all_key_words = []
    for word in cla_Key_words:
        try:
            if model.similarity(str("节日"),str(word)) < 0.4:
                continue
            all_key_words.append(word)
            simi_words = model.most_similar(str(unicode(word)))
        except KeyError:
            continue
        for w in simi_words:
            all_key_words.append(w[0])
    all_key_words = list(set(all_key_words))
    all_key_words = extend_Word(model,all_key_words)
    # write to file
    with open(MyCode.config.ResultFilePath+ "Topic_festival.txt", 'w') as fp:
        for key_word in all_key_words:
            fp.writelines(key_word+"\n")

# extends words
def extend_Word(model,simi_words):
    # extendWords = []
    new_len = len(simi_words)
    pre_len = 0
    item = 0
    while math.fabs(new_len-pre_len)/new_len > 0.1:
        extendWords = simi_words
        for w in xrange(len(simi_words)):
            try:
                extends = model.most_similar(unicode(simi_words[w]))
                for e in extends:
                    if e[1] > 0.8:
                        extendWords.append(e[0])
            except KeyError:
                continue
        simi_words = list(set(extendWords))
        pre_len = new_len
        new_len = len(simi_words)
        item += 1
        if item >= 1:
            break
    print "finished extends!"
    return simi_words


def main():
    # getFileContext_Participle()
    # getTxtFileSentence()
    model = buildModel("wordRank_new_1")
    # print model.
    print model

    # words = extend_Word(model,[u'立春',u"立夏"])
    words_sets_1 = set(model.most_similar([u'春分'],topn=200))
    words_sets_2 = set(model.most_similar([u"夏至"],topn=200))
    words_sets_3 = set(model.most_similar([u"立秋"],topn=200))
    words = list(words_sets_1&words_sets_2)
    print len(words)
    words = list(words_sets_1&words_sets_3)
    print len(words)
    print model.similarity(u"春分",u"立冬")
    # words = model.most_similar([u"中国",u"美国",u"英国",u"韩国",u"印度",u"瑞士"],topn=100)
    # words = model.most_similar([u"春节",u"端午节",u"中秋节",u"劳动节"], topn=100)
    words = model.most_similar([u"花",u"芍药花",u"茉莉花"], topn=100)
    # u"夏至", u"立秋", u"冬至"
    # words = model.most_similar(["自杀"], topn=1000)
    for w in words:
        print w[0],":",w[1]
    # print model
    # for words in words_sen:
    #     for i in xrange(len(words)-1):
    #         similarly(model,words[i],words[i+1])
    #
    #     print
    # for w in wnew_words:
    #     sim_ws = model.most_similar([unicode(w)])
    #     print w,"相似词有："
    #     for sw in sim_ws:
    #         print sw[0],":",sw[1]
    #     print
    # for i, topic_dist in enumerate(topic_word):
    #     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    #     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    #
    #
    # plt.plot(model.loglikelihoods_[5:])
    # plt.show()
    print 'Ok'



if __name__ == '__main__':
    main()

