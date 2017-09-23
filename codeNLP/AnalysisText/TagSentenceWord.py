# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-20

# today  i want to write my first code file in company
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import  nltk
from MyCode.tools import Participle, ReadFile
import math
import jieba.analyse
from nltk.corpus import sinica_treebank
import MyCode.config

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 获取文件文本，并词切分，以句子为单位切分 from Excel
# 返回句子的切分结
def buildWordfromExcel():
    file = "../Data/Sentence_QR_pair_0714.xlsx"
    Q_s,R_s = ReadFile.getFileSentence(file)
    sentences = Participle.Participle(Q_s)
    Q_sentences = []
    for s in sentences:
        snetence = ''
        for word in s:
            snetence += word + ' '
        Q_sentences.append(snetence)
    return Q_sentences

#用print输出本地字符格式
def dump_result(result):
    i = 0
    for item in result:
        print item[0],",",item[1],";",
        if i != 0 and i % 5 == 0:
            print
        i += 1
    print

#获取文件的文本 并切词 from TXT
def buildWordFromTxt():
    file = "../Result/sentence1.txt"
    sentences = ReadFile.readTXTFile(file)
    par_Sentences = []
    par_Sentences = Participle.Participle(sentences[10000:11000])
    w_Sentence = []
    with open("../Result/fenci.txt",'w') as fp:
        for s in par_Sentences:
            p_sentence = ''
            for word in s:
                p_sentence += word + ' '
            w_Sentence.append(p_sentence)
        # print 'Start writing ... ...'
        # fp.writelines(w_Sentence)
        # print 'Finished writing !'
    return w_Sentence

# word tag model
def Tag_Word_model():
    sinica_treebank_tagged_sents = sinica_treebank.tagged_sents()
    size = int(len(sinica_treebank_tagged_sents) * 0.9)
    train_sents = sinica_treebank_tagged_sents[:size]  # 90%数据作为训练集
    test_sents = sinica_treebank_tagged_sents[size:]  # 10%数据作为测试集
    t0 = nltk.DefaultTagger('Nab')  # 词性的默认值为名词
    # t1 = nltk.pos_tag(train_sents,str="cn")
    t1 = nltk.UnigramTagger(train_sents, backoff=t0)  # 一元标注
    t2 = nltk.BigramTagger(train_sents, backoff=t1)  # 多元（二元）标注
    # dump_result(t2.tag(test_sents))
    print t2.evaluate(train_sents)  # 根据带标注的文本，评估标注器的正确率
    return t2


# word tag
def Tag_Word(sentence,model):
    tokens = nltk.word_tokenize(sentence)
    return model.tag(tokens)

def tag_Sentences_Word(Sentences):
    tag_Sentences = []
    model = Tag_Word_model()
    for sentence in Sentences:
        tag_Sentence = Tag_Word(sentence,model)
        tag_Sentences.append(tag_Sentence)
        dump_result(tag_Sentence)
    return tag_Sentences

# tf-idf 计算该值 提取关键词
def caltf_idf_Word_Counter(Sentences):
    word_Counts = []
    for s in Sentences:
        word_Counts.append(nltk.Counter(nltk.word_tokenize(s)))
    return word_Counts

def tf(word, count):
    return count[word] / sum(count.values())

def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)

def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))

def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)

# for test
def cal_tf_idf(count_list):
    countlist = count_list[:10]
    for i, count in enumerate(countlist):
        # print count.values()
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:3]:
            print("\tWord: %s, TF-IDF: %lf"%(word, round(score, 3)))

#for test buildWord
def printWordSentence(Sentences):
    for sen in Sentences:
        print sen


def getTag_lab(tag_Sentences):
    tagLabs = []
    for tag_sentence in tag_Sentences:
        for item in tag_sentence:
            tagLabs.append(item[1])
    return list(set(list(tagLabs)))

def writeFenci(fenci_sentence):
    with open("../Result/fenci.txt","w") as fp:
        fp.writelines(fenci_sentence)

def readfenciFile_Word():
    word_sentences = []
    with open("../Result/fenci.txt","r") as fp:
        line = fp.readline()
        # i = 0
        while line:
            # if i > 100:
            #     break
            # i += 1
            word_sentence = line.split("\n")[0]
            word_sentences.append(unicode(word_sentence))
            line = fp.readline()
    return word_sentences

# input sentences
def get_tagByjieba(sentences):
    tag_Sentences = []
    length = len(sentences)
    print "共有问句：",length
    i = 0
    for sen in sentences:
        print sen
        tag_Sentences.append(jieba.analyse.extract_tags(sen))
        if i % 10000 == 0:
            print '已完成',float(i)/length,"%"
        i += 1
    return tag_Sentences

#write result to file
def writeToFile(sentence,tag_key_words_sentences):
    fp = open(MyCode.config.SentenceKeyWordPath + "key_word_result.txt", 'w')
    i = 0
    for i in xrange(len(tag_key_words_sentences)):
        print u"第" + str(i + 1) + u"句 : \"" + str(sentence[i].split('\n')[0]) + u"\"的关键词有：",
        fp.write(u"第" + str(i + 1) + u"句 : \"" + str(sentence[i].split('\n')[0]) + str("\"的关键词有："))
        for word in tag_key_words_sentences[i]:
            print word,
            fp.write(str(word) + " ")
        print ''
        fp.write("\n")
        i += 1
    fp.close()

#tag used pos_tag
def tagger_sentence_word():
    # sentences = ReadFile.readTXTFile("../Result/sentence1.txt")
    sentences = buildWordFromTxt()
    for sen in sentences:
        tocken = nltk.word_tokenize(unicode(sen))
        tagged_words = nltk.pos_tag(tocken)
        # print tagged_words
        print sen," 标注结果:",
        for tag_word in tagged_words:
            print tag_word[0],tag_word[1],";",
        print
        # re = nltk.ne_chunk(tagged_words)
        # print re

# 提取句子 关键词
def ExtracKeyWordFromSentence(sentencefile =MyCode.config.SentenceKeyWordPath + "badcase.xlsx"):
    print "Extrc key words from sentence"
    sentences = ReadFile.getFileSentence(sentencefile)[0]
    sentences = list(set(sentences))
    tag_sentence = get_tagByjieba(sentences)
    writeToFile(sentences,tag_sentence)
    sentences_keywords = []
    for i in xrange(len(sentences)):
        sentences_keywords.append((sentences[i],tag_sentence[i]))
    return sentences_keywords

# for test
def main():
    #关键词提取
    # sentences = ReadFile.readTXTFile(config.ResultFilePath+"sentence1.txt")
    # sentences = ReadFile.getFileSentence(config.SentenceKeyWordPath+"badcase.xlsx")
    # print "Start tagger ......"
    # sentences = list(set(sentences[0]))
    # tag_Sentences = get_tagByjieba(sentences)
    # print "Finished tagger "
    # writeToFile(sentences,tag_Sentences)

    ##关键词提取
    ExtracKeyWordFromSentence()

    #文本标注
    # print "Start tag word ... ..."
    # tocken_Sentences = buildWordFromTxt()
    # # tocken_Sentences = ReadFile.readTXTFile("../Result/sentence1.txt")
    # print "tagging ... ..."
    # tag_Sentences = nltk.pos_tag(tocken_Sentences)
    # print "finished tag."
    # with open("../Result/tag_result.txt",'w') as tagFp:
    #     for tag_sentence in tag_Sentences:
    #         print tag_sentence
    #         for item in tag_sentence:
    #             tagFp.write(item[0]+":"+item[1]+" ; ")
    #         tagFp.write("\n")
    # model = Tag_Word_model()
    # dump_result(tag_Sentences_Word(tocken_Sentences))

    # print 2
    #   文本标注2
    # tagger_sentence_word()




if __name__ == '__main__':
    main()


    # print "范冰冰 和 陈小春的相似度：",model.similarity('范冰冰','陈小春')

