# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-31

# function  解决LDA 的话题分析数据处理以及数据矩阵构建

import  sys
sys.path.append('../..')
reload(sys)
from MyCode.tools import ReadFile
import numpy
import  lda
import pickle
from MyCode import config
import logging
import gensim
from MyCode.tools.WriteResult import WriteResult
from MyCode.tools import Participle
from MyCode.tools import filterStopWords
from MyCode.tools.Show import Show

logging.basicConfig(filename='logger.log',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 获取数据文件,已分词文件
# 返回句子分词矩阵
def getFileSentences(subfilename = "souhu_fenci"):
    sentences = ReadFile.read_souhu_fenci_file(subfilename=subfilename)
    logging.info("data size :%d"%len(sentences))
    print("data size :%d"%len(sentences))
    par_sentences = []
    for sentence in sentences:
        snetence_words = sentence.split(" ")
        par_sentences.append(snetence_words)
    return par_sentences

# 词列表
def buildWordList(par_sentences):
    word_list = []
    for par_sentence in par_sentences:
        for word in par_sentence:
            word_list.append(word)
    word_list = list(set(word_list))
    return word_list

# 构建词典
def buildWord_dic(documents):
    # filename = config.CorpusFilePath+"word_dic.txt"
    # documents = getFileSentences()
    id2word = gensim.corpora.Dictionary(documents=documents)
    # wr = WriteResult()
    # wr.WriteSingleDic(id2word,filename)
    # wr.WriteValueToFile(id2word,"id2word")
    return id2word

# 加载词典
def load_word_dic(word_model = "id2word_2"):
    id2word = None
    try:
        print "load word dic"
        with open(config.ModelPath + word_model+".model", "rb") as fp:
            id2word = pickle.load(fp)
            logging.info("load word dic success")
        print "load success"
    except:
        print "build word dic"
        documents = getFileSentences()
        id2word = buildWord_dic(documents)
        logging.info("build finished and write dic to file")
        print "build finished and write dic to file"
        with open(config.ModelPath + word_model +".model", 'wb') as fp:
            pickle.dump(id2word, fp)
    print len(id2word.keys())
    return id2word

# 加载语料
def buildLdaModel(docments,dic,num_topics = 10):
    filename = config.CorpusFilePath+'Corpus_train.txt'
    trainCorpus = [dic.doc2bow(docment) for docment in docments]
    tfidf = gensim.models.TfidfModel(trainCorpus)
    corpustfidf = tfidf[trainCorpus]
    lda_model = gensim.models.LdaModel(corpus=corpustfidf,id2word=dic,num_topics=num_topics)
    return lda_model

#
def getWordsId(document,dic):
    documentId = dic.doc2bow(document)
    return documentId


# build word dic
def buildWordDic(word_list):
    dic = {}
    for i in xrange(len(word_list)):
        dic.setdefault(word_list[i],i)
    return dic

# 构建模型矩阵
def buildMatrix(par_sentences,word_list):
    n_doc = len(par_sentences)
    m_feature = len(word_list)
    X = numpy.zeros((n_doc,m_feature),dtype=numpy.int)
    # 构建词字典映射
    dic = buildWordDic(word_list)
    for i in xrange(n_doc):
        for word in par_sentences[i]:
            X[i][dic.get(word)] += 1
    return X,dic

def LDATipicModel(modelname = "LDATopicWord_2"):
    try:
        print "Load LDA Model ... ..."
        with open(config.ModelPath + modelname + ".model", 'rb') as pkl_file:
            Lda_model = pickle.load(pkl_file)
        print "Load Model success"
    except:
        print "Train LDA Model ... ..."
        logging.info("加载数据")
        sentences = getFileSentences(subfilename="souhu_fenci_no_filter")
        # sentences = ReadFile.getQueriesSentence(config.SimilarlySentencePath + "AllQueriesWithID.txt")
        # doc_sentences = getQueries(sentences)
        logging.info("构建词典")
        id2word = load_word_dic()
        num_topics = 100
        logging.info("训练模型")
        Lda_model = buildLdaModel(sentences,id2word,num_topics)

        logging.info("存储模型{0}".format(modelname))
        print "Finished Train LDA Model and saving ... ..."
        with open(config.ModelPath+modelname+".model","wb") as model_fp:
            pickle.dump(Lda_model,model_fp)
        print "Finished save LDA Model"
    return Lda_model

def getDocumentTopic(document,lad_model):
    return lad_model.get_document_topics(document)

# 处理语句成query
def getQueries(sentences):
    par_sentences = Participle.Participle(sentences)
    # thl = thulac.thulac()
    # par_sentences = [thl.cut(sen.encode("utf-8")) for sen in sentences]
    # documents = filterStopWords.filterStopWordFromSentences(par_sentences)
    documents = par_sentences
    return documents

# 处理query 的相似性
def getQueriySimilarly(queries):
    # logging.info("")
    word_dic = load_word_dic()

    lda_Model = LDATipicModel()

    docs_topic = [lda_Model.get_document_topics(getWordsId(doc, word_dic),minimum_probability=0.1) for doc in queries]
    # docs_topic = [getDocumentTopic(doc_id, lda_Model) for doc_id in documents_id]
    return docs_topic

# 同类别归类
def groupByTopic(docs_topic,sentences):
    results = {}
    i = 0
    cannotRecgnize = []
    for doc in docs_topic:
        if len(doc) == 0:
            cannotRecgnize.append(sentences[i])
            i+=1
            continue
        if doc[0][0] in results:
            results[doc[0][0]].append((sentences[i],doc[0][1]))
        else:
            results[doc[0][0]] = [(sentences[i],doc[0][1])]
        i += 1
    Wr = WriteResult()
    Wr.WriteCanRecgnize(cannotRecgnize)
    return results


def main():
    # 老版本
    # Lda_model = LdaTopic(modelName='LDAsimiWord_5')
    # # print Lda_model[0]
    # lda_model = Lda_model[0]
    # words = Lda_model[1]
    # n_top_words = 1
    # for i ,topic_dist in enumerate(lda_model.topic_word_):
    #     topic_words = numpy.array(words)[numpy.argsort(topic_dist)][:n_top_words:-1]
    #     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    #
    # Lda_model2 = LdaTopic(modelName='LDAsimiWord_6')
    # # print Lda_model[0]
    # lda_model2 = Lda_model2[0]
    # words2 = Lda_model2[1]
    # n_top_words2 = 1
    # for i, topic_dist in enumerate(lda_model2.topic_word_):
    #     topic_words = numpy.array(words2)[numpy.argsort(topic_dist)][:n_top_words2:-1]
    #     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    # documents = getFileSentences()

    # sentences = [u"你知道周杰伦是谁么？",u"周杰伦是谁？",u"你知道周杰伦吗？",u"你认识周杰伦吗？",u"你认识周杰伦么？",u"你知道周杰伦么？",\
    #              u"周杰伦知道么？",u"周杰伦知道是谁么？",u"周杰伦知道吗",u"周杰伦知道是谁吗？",u"周杰伦是谁？",u"周杰伦你认识么？",u"周杰伦你知道是谁么？",\
    #              u"周杰伦你认识吗？",u"周杰伦你知道是谁吗？",u"你认识周杰伦吗？",u"你知道周杰伦吗？",u"你知道周杰伦么？",u"你认识周杰伦么？",u"你认识周杰伦吗？",\
    #              u"你认识周杰伦是谁么？",u"你认识周杰伦是谁吗？",u"你知道周杰伦吗？",u"你知道周杰伦是谁吗？",u"你知道周杰伦是谁么？"]
    sentences = ReadFile.readTXTFile("./BitermTopicModel/document_corpus.txt")

    queries = getQueries(sentences[:100])
    for query in queries:
        for q in query:
            print q,
        print
    docs_topic = getQueriySimilarly(queries)
    # for topic in docs_topic:
    #     for re in topic:
    #         print re,1
    #     print
    results = groupByTopic(docs_topic,sentences)
    sh = Show()
    sh.showDocTopicResult(results)
    Wr = WriteResult()
    Wr.WriteTopicResult(results)

    #

if __name__ == '__main__':
    main()


