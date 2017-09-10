# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-04

# function  添加语料到相关问题的语料库

import os
import sys
sys.path.append('..')
import ReadFile
import config
import xlrd

def getKeyWordsAndResponses(file):
    dataFilePath = config.InputDataFilePath
    resultFile  = config.InputDataFilePath
    bk,table_names = ReadFile.readCorpusExcel(dataFilePath+'badcase/'+file+'.xlsx')
    for name in table_names:
        table = bk.sheet_by_name(name)
        sentences = getTableContext(table)

        AddCorpus(sentences,name)


def getTableContext(table):
    sentences = []
    for i in xrange(table.nrows):
        if i == 0:
            continue
        sen = table.row_values(i)[1:5]
        sentences.append(sen)
    return sentences

def AddCorpus(sentences,name):
    old_sentences = ReadFile.readTXTFile(config.RegularsFilePath+name+'.query.txt')
    old_R_sentences = ReadFile.readTXTFile(config.RegularsFilePath+name+".response.txt")
    count = len(old_sentences)+1
    for sentence in sentences:
        contain = False
        Id = name
        for o_sen in old_sentences:
            lines = o_sen.split('\t')
            if lines[1][:-1] == sentence[0]:
                contain = True
                Id = lines[0]
                break
        if not contain:
            Id += '%05d'%count
            count += 1
            old_sentences.append(Id+'\t'+sentence[0]+'\n')
        for response in sentence[1:4]:
            if response != '' or response != '\n' or response != '\t' or len(response) > 2:
                old_R_sentences.append(Id+'\t'+response+'\n')
    # write to file
    with open(config.ResultFilePath+name+".query.txt",'w') as fp:
        for line in old_sentences:
            fp.write(line)

    with open(config.ResultFilePath+name+".response.txt",'w') as fp:
        for line in old_R_sentences:
            fp.write(line)

def main():
    getKeyWordsAndResponses("corpus-20170808")

if __name__ == '__main__':
    main()


