# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-24

# today  i want to write my first code file in company


def check_contain_chinese(check_str):
     for ch in check_str.decode('utf-8'):
         if u'\u4e00' <= ch <= u'\u9fff':
             return True
     return False

def InputFileProcess():
    fwfp = open("../Result/corpus.txt","w")
    with open("../Data/corpus_lgy.txt",'r') as fp:
        line = fp.readline()
        while line:
            line = line.replace("<content>",'')
            line = line.replace('</content>','')
            if len(line) > 5:
                fwfp.write(line)
            line = fp.readline()
    fp.close()

# 句子过滤 sentences filter remove contecxt latter '\t'
def removeContext(Sentences):
    new_sentences = []
    for sentence in Sentences:
        line = sentence.split("\t")[0]
        new_sentences.append(line)
    return new_sentences

def getWordsFromSentences(sentences):
    Words = []
    for sentence in sentences:
        for w in sentence:
            Words.append(w)
    return list(set(Words))

def main():
    InputFileProcess()

if __name__ == '__main__':
    main()