# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-10

class Show():
    def __init__(self):
        pass

    def showSenetenceStructResult(self,sentence_class_list):
        for sentence_class in sentence_class_list:
            # for sen in sentence_class
            print "class type:",
            for w in sentence_class[0]:
                print w[1],
            print
            for sen in sentence_class:
                for w in sen:
                    print w[0],
                print

    def showClusterResult(self,clusters_set):

        for key in clusters_set.keys():
            clusters = clusters_set[key]
            i = 0
            print "类别%s的细分项目有：\n"%key
            for cluster in clusters:
                if len(cluster) <= 0:
                    continue
                print "{:02d}".format(i+1)+"词类:"
                for word in cluster:
                    print word,
                print
                i += 1

    def showClassExtend(self,extend_Words):
        for key in extend_Words:
            print key,extend_Words[key]
            
    def showDocTopicResult(self,results):
        for topic in results:
            print "主题{0}：".format(topic)
            for sen in results[topic]:
                print sen[0], sen[1]
            print 
            

        
