# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-10

import codecs
from MyCode import config
import time
import pickle
import codecs

class WriteResult():
    """写文件，将处理结果写入到制定文件"""
    def __init__(self):
        pass

    def WriteSentences(self,sentences, file = config.TopicFilePath + "train_sentences.txt"):
        with codecs.open(file, 'w', encoding='utf-8') as fp:
            for sen in sentences:
                fp.write(sen.strip()+"\n")

    def WriteSentenceStruct(self,sentence_class_list):
        with codecs.open(config.QueryPath+ 'SentenceStructResult.txt', 'w', encoding='utf-8') as fp:
            for sentence_class in sentence_class_list:
                fp.write("class type: ")
                for w in sentence_class[0]:
                    fp.write(w[1]+" ")
                fp.write("\n")
                for sen in sentence_class:
                    for w in sen:
                        fp.write(w[0]+" ")
                    fp.write('\n')

    def WriteSentenceTemplate(self,sentences):
        with codecs.open(config.QueryPath+ "SentenceTemplate"+str(time.strftime("%Y_%m_%d_%H_%M", time.localtime()))+ ".txt", 'w', encoding='utf-8') as fp:
            sorted_sens = sorted(sentences.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
            for sentence in sorted_sens:
                if sentence[1] >= 3:
                    fp.write(sentence[0]+"\t"+str(sentence[1])+"\n")

        return

    def WriteTemplate(self,tem_s):
        with codecs.open(config.QueryPath+ "Template"+str(time.strftime("%Y_%m_%d_%H_%M", time.localtime()))+ ".txt", 'w', encoding='utf-8') as fp:

            i = 0
            for cluster in tem_s:
                i += 1
                if len(cluster) <= 2:
                    continue
                fp.write("cluster_template %02d\n"%i)
                for sen in enumerate(cluster):
                    # print(sen)
                    fp.write(sen[1]+'\n')

        return

    def writeClusterResult(self,clusters_set,file='WordClusterRefine.txt'):
        dirPath = config.WordClusterPath
        with open(dirPath+file,'w') as fp:

            for key in clusters_set.keys():
                i = 0
                clusters = clusters_set[key]
                fp.write("类别%s的细分项目有：\n"%key)
                for cluster in clusters:
                    if len(cluster) <= 0:
                        continue
                    fp.write("{:02d}".format(i+1)+"词类:")
                    for word in cluster:
                        fp.write(word+" ")
                    fp.write("\n")
                i +=1

    def writeClassExtendResult(self,extend_Words,file='WordExtends.txt'):
        dir = config.WordClusterPath
        with open(dir+file,"w") as fp:
            for key in extend_Words:
                fp.write(key+" "+extend_Words[key]+"\n")

    def WriteSingleDic(self,dic,filename):
        with open(filename,"w") as fp:
            for key in dic:
                fp.write(str(key)+"\t"+str(dic[key]+"\n"))

    def WriteValueToFile(self,model,file="Data_X"):
        file = config.ModelPath+file+".model"
        with open(file,'wb') as fp:
            pickle.dump(model,fp)

    def WriteResultAnswer(self,pre_data=None,pre_anwser=None,file=None):
        if not file:
            file = config.ResultPath+"result.csv"
        add = None
        print "answer:",len(pre_anwser),"data:",len(pre_data)
        length = 0
        if len(pre_data) <= len(pre_anwser):
            length = len(pre_data)
        else:
            length = len(pre_anwser)

        with open(file,"a+") as fp:
            # fp.write("orderid,geohashed_end_loc1,geohashed_end_loc2,geohashed_end_loc3")
            for i in xrange(length):
                # print i,pre_data[i][0]
                # print pre_anwser[i]
                fp.write(pre_data[i][0]+","+pre_anwser[i][0]+","+pre_anwser[i][1]+","+pre_anwser[i][2]+"\n")

    def WriteTopicResult(self,results,file=config.SimilarlySentencePath+"topic_sentence.txt"):
        with codecs.open(file,"w",encoding='utf8') as fp:
            for topic in results:
                fp.write("主题{0}：\n".format(topic))
                for sen in results[topic]:
                    fp.write("{0},{1}\n".format(sen[0],sen[1]))
                fp.write("\n")

    def WriteCanRecgnize(self,sentences):
        with codecs.open(config.SimilarlySentencePath+"candealSentences.txt","w",encoding='utf8') as fp:
            for sen in sentences:
                fp.write(sen+"\n")

    def WriteSimilarlySentence(self,result,file = config.SimilarlySentencePath+"SimilarlySentences.txt"):
        with codecs.open(file, "w", encoding='utf8') as fp:
            for sen in result:
                fp.write(sen + " ::的相似句包括\n")
                simi_sentences = result[sen]
                for sentence in simi_sentences:
                    fp.write(sentence.strip()+"\n")
                fp.write("\n\n")

    def WriteSimilarSentence(self,result,file = config.SimilarlySentencePath+"SimilarlySentences.txt"):
        with codecs.open(file, "w", encoding='utf8') as fp:
            for sen in result:
                fp.write(sen + " ::的相似句包括\n")
                simi_sentences = result[sen]
                for sentence in simi_sentences:
                    fp.write(sentence[0].strip()+"-->(相似度)::"+str(sentence[1])+"\n")
                fp.write("\n\n")

