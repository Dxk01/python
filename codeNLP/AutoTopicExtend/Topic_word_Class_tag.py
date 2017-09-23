# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-26

import MyCode.ExtendWords.similarlyWord
from MyCode.tools import ReadFile


def getTopicKeyWord(Topic):
    keyWords = ReadFile.readTXTFile("../Result/Topic_%s.txt" % Topic)
    key_words = []
    for word in keyWords:
        key_words.append(word.split("\n")[0])
    return key_words

#获取词的类别字典
def getAllWordClass():
    # all_Word_lines = ReadFile.readTXTFile("../Data/semantic_wordgroup_new.txt")
    with open("../Data/semantic_wordgroup_new.txt",'r') as fp:
        line = fp.readline()
        words_dic = {}
        while line:
            word = line.split(' ')
            if words_dic.has_key(word[0]) == 0:
                words_dic.setdefault(word[0],word[1])
            line = fp.readline()
        return words_dic

# 获取近义词类别
def getSimilaryClass(word,words,simi_words):
    model = MyCode.ExtendWords.similarlyWord.buildModel()
    max_simiv = 0
    simi_word = words[0]
    for w in words :
        if w in simi_words or  w == word:
            continue
        try:
            cur_simiv = model.similarity(w,word)
            if cur_simiv > max_simiv:
                max_simiv = cur_simiv
                simi_word = w
        except :
            continue
    return simi_word

# 查询字典标记词类别
# 将结果写入文件
def Word_Class_tag(words,words_dic,Topic='festival'):
    with open("../Result/Topic_%s_Class.txt"%Topic,'w') as fp:
        semfp = open("../Data/semantic_wordgroup_new.txt",'a+')

        for word in words:
            if words_dic.has_key(word):
                fp.write(word+" "+words_dic.get(word))

            # else:
                # fWords = words
                simi_words = []
                # simi_word = getSimilaryClass(word, words,simi_words)
                # print word, simi_word
                # if words_dic.has_key(simi_word) == 0:
                #     continue
                # print word, simi_word,"write"
                # words_dic.setdefault(word,words_dic.get(simi_word))
                # semfp.write(word+" "+words_dic.get(simi_word)+'\n')
                # fp.write(word + " " + words_dic.get(simi_word) + "\n")
        semfp.close()

def main():
    words_dic = getAllWordClass()
    words = getTopicKeyWord("festival")
    print 'start ... ...'
    Word_Class_tag(words,words_dic,"festival")
    print 'ok'

if __name__ == '__main__':
    main()