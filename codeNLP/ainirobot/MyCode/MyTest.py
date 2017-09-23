# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-10

import sys
sys.path.append("/Users/orion/PycharmProjects/Chat/chat_system/chatter.v2/chatter/Algorithm")
sys.path.append("../..")
reload(sys)

from MyCode.AnalysisText.SentenceStruct import SentenceStruct
from MyCode.AnalysisText.sentence_tag import Sentence_Tag
from MyCode.ExtendWords import ClassRefine
from MyCode.ExtendWords.ClassExtend import WordClassify
from MyCode.tools import ReadFile
from MyCode.tools.Show import Show
from MyCode.tools.WriteResult import WriteResult
from MyCode import config
from QueryTest.QueryTest import QueryTest
from MyCode.Algorithm.LDA import LDA
from MyCode.tools.LineSetence import LineSentence
from MyCode.Topic.TopicTransition import TopicTransition
from MyCode.Algorithm.HDA import HDA
from MyCode.tools import preProcess

class MyTest():
    def __init__(self,model=None):
        self.model = model

    def TagSenetnceTest(self,method=2):
        tag_sentence = Sentence_Tag()
        sentences = ReadFile.getQueriesWithId('AllQueriesWithID')
        re_sentences = tag_sentence.tagSentences(sentences[:100],method=method)
        for sen in re_sentences:
            if method == 1:
                for w in sen:
                    print w[0],w[1]
                print
            else:
                print sen

    def TestSentencesStruct(self):
        method = 2
        tag_sentence = Sentence_Tag()
        sentences = ReadFile.getQueriesWithId('AllQueriesWithID')
        sentenceStruct = SentenceStruct()

        tag_sentences = tag_sentence.tagSentences(sentences,method)
        sentences_class_list = sentenceStruct.SimiSentenceStruct(tag_sentences)
        # sh = Show()
        # sh.showSenetenceStructResult(sentences_class_list)
        # wr = WriteResult()
        # wr.WriteSentenceStruct(sentences_class_list)
        return sentences_class_list

    def TestSentenceTem(self):
        sentences_class_list = self.TestSentencesStruct()
        St = SentenceStruct()
        sentence_tem = St.SentenceStructExtract(sentences_class_list)
        wr = WriteResult()
        # wr.WriteSentenceTemplate(sentence_tem)
        template_s = St.SentenceStructExtractTem(sentence_tem)
        wr.WriteTemplate(template_s)

    def TestWordClusters(self):
        cr = ClassRefine.ClassRefine()
        words = cr.getWords()
        Cluster_sets = cr.ClassifyWord(words)
        show = Show()
        show.showClusterResult(Cluster_sets)
        wR = WriteResult()
        wR.writeClusterResult(Cluster_sets)

    def TestClassExtend(self):
        Wcf = WordClassify()
        words = Wcf.getNewWords()
        extend_words = Wcf.wordClassify(words)
        show = Show()
        show.showClassExtend(extend_words)
        Wr = WriteResult()
        Wr.writeClassExtendResult(extend_Words=extend_words)

    def QueryResponseTest(self,sentence=None,train_sentences=None):
        if sentence is None:
            return
        queries = self.model.calSentenceSimilarly(sentence=sentence,num_best=1)[0]
        qt = QueryTest()
        print int(queries[0])
        query_sentences = train_sentences[int(queries[0])]
        qt.queryTest(query_sentences)


    def TestTopicLda(self,sentences=None):
        Lda_topic = LDA("test_lad","test_lda_word")
        docs = LineSentence(sentences)
        Lda_topic.build_word_dic(docs)
        Lda_topic.buildModel(docs,num_topics=100)
        Lda_topic.show()

    def TestLdaLoad(self):
        Lda_topic = LDA("test_lad", "test_lda_word")
        Lda_topic.load_LdaModel()
        Lda_topic.show()

    def TestTopicLdaSentence(self,sentence=None):
        if sentence is None or sentence == '':
            return None,None
        doc_topic = self.model.getQuerySimilarly(sentence)
        if doc_topic == None or len(doc_topic) == 0:
            return None,None
        for topic in doc_topic:
            return topic[0],topic[1]

    def TestTopicTransition(self):
        topic = TopicTransition()
        topic.load()
        print topic.transitionByProbility(1)

    def TestTopicHda(self,sentences=None):
        Lda_topic = HDA("test_Hda", "test_Hda_word")
        docs = LineSentence(sentences)
        Lda_topic.buildModel(docs)
        Lda_topic.show()

    def TestTopicHdaSentence(self,sentence=None):
        doc_topic = self.model.getQuerySimilarly(sentence)
        if len(doc_topic) == 0 or doc_topic == None:
            return None,None
        for topic in doc_topic:
            return topic[0],topic[1]

    def TestBuildModelLda(self,sentences):
        base_model_name = "test_Lda_"
        Lda_topic = LDA(base_model_name,"test_lda_worddic")
        docs = LineSentence(sentences)
        Lda_topic.build_word_dic(docs)
        for i in xrange(10):
            modelName = base_model_name+"%02d"%i
            print "build Lda model {0}".format(modelName)
            Lda_topic.setModelName(modelName)
            Lda_topic.buildModel(documents=docs,num_topics=(i+1)*100)

    def TestModelclassLda(self,sentences):
        base_model_name = "test_Lda_"
        # Lda_topic = LDA(base_model_name, "test_lda_worddic")
        # Lda_topic.load_word_dic()
        for x in xrange(10):
            modelName = base_model_name+"%02d"%x
            print "Load LDA model {0}".format(modelName)
            Lda_topic = LDA(base_model_name, "test_lda_worddic")
            Lda_topic.load_word_dic()
            Lda_topic.setModelName(modelName)
            Lda_topic.load_LdaModel()
            self.model = Lda_topic
            Wr = WriteResult()
            result = {}
            for sen in sentences:
                topic_id,simi_v = self.TestTopicLdaSentence(sentence=sen.strip())
                if topic_id == None or simi_v == None:
                    continue
                if topic_id not in result:
                    result[topic_id] = []
                result[topic_id].append((sen.strip(),simi_v))
            Wr.WriteTopicResult(result,config.TopicFilePath+"lda_topic_{0}.txt".format(x))



def main():
    # Lda_topic = HDA("test_Hda", "test_Hda_word")
    # # Lda_topic = LDA("test_lad", "test_lda_word")
    # Lda_topic.load_word_dic()
    # # Lda_topic.load_LdaModel()
    # Lda_topic.load_HDAModel()
    # Lda_topic.show()
    sentences = ReadFile.readTXTFile(config.TopicFilePath + "train_sentences_3.txt")

    # train_sentences = []
    # for sen in sentences:
    #     if preProcess.check_contain_chinese(sen.strip()) and len(sen) > 4:
    #         train_sentences.append(sen)
    # print len(train_sentences)
    # train_sentences = list(set(train_sentences))
    # wr = WriteResult()
    # wr.WriteSentences(train_sentences,config.TopicFilePath+"train_sentences_3.txt")
    print len(sentences)
    mtest = MyTest()
    # mtest.TestBuildModelLda(sentences[:1000])
    mtest.TestModelclassLda(sentences[:1000])
    # test.TagSenetnceTest()
    # sentences_class_list = test.TestSentencesStruct()
    # sentences_tem = test.
    #
    # test.TestSentenceTem()
    # print Ls.distance("r有n吗w","rn是rw")
    #
    # test.TestWordClusters()
    #
    # test.TestClassExtend()
    # test.TestWordRanker()
    # [u"我居然跟你聊，我也是醉了","你身体好吗"]
    # test_sentences = ReadFile.readTXTFile(config.QueryTestPath+"test.txt")
    # for sen in test_sentences:
    #     print sen
    #     mtest.QueryResponseTest(sen,train_sentences)
    # mtest.TestTopicHda(sentences[:1000])

    # mtest.TestTopicHda()



    # mtest.TestTopicTransition()
    # mtest.TestLdaLoad()
    # mtest.TestTopicHda(train_sentences)

if __name__ == '__main__':

    main()
