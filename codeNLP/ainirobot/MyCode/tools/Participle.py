# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-20

# today  i want to write my first code file in company

import jieba

import MyCode.tools.ReadFile


# participle document word
def Participle(Sentences):
    # par_Sentences = p[]
    sentences = []
    for sentence in Sentences:
        sentences.append(jieba.cut(sentence,cut_all=False))
    return sentences

# for test
def main():
    tables = MyCode.tools.ReadFile.readExcel("../Data/Mid_result/Sentence_QR_pair_0714.xlsx")
    Q_Sentences,R_Sentences = MyCode.tools.ReadFile.getSentence(tables)

    par_Sentences = Participle(Q_Sentences)
    for sentence in par_Sentences:
        for word in sentence:
            print word

if __name__ == '__main__':
    main()