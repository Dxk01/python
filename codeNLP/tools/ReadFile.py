# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-07-20

# today  i want to write my first code file in company

import sys
sys.path.append("../../")
reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
from os import listdir
from os.path import isfile,join
import preProcess
import xlrd
from MyCode import config
import codecs
import pickle

def readCorpusExcel(file):
    bk = xlrd.open_workbook(file)
    table_names = bk.sheet_names()
    return bk,table_names

#read Excel corpus data
def readExcel(file):
    bk = xlrd.open_workbook(file)
    table_names = bk.sheet_names()
    tables = []
    for table_name in table_names:
        table = bk.sheet_by_name(table_name)
        tables.append(table)
    return tables

#
def readTXTFile(file):
    sentences = []
    with codecs.open(file,'r',encoding='utf-8') as fp:
        line = fp.readline()
        while line:
            sentences.append(line)
            line = fp.readline()
    return sentences

# get corpus sentences QR pairs
def getSentence(tables):
    Q_sentences = []
    R_sentences = []
    for table in tables:
        for i in xrange(table.nrows):
            line = table.row_values(i)[0]
            Q_sentences.append(line.strip())
    return Q_sentences,R_sentences

def getFileSentence(file="../Data/corpus/Sentence_QR_pair_0714.xlsx"):
    tables = readExcel(file)
    Q_s,R_s = getSentence(tables)
    return Q_s,R_s

def getCorpusFromExcel(file=config.SimilarlySentencePath+'corpus_0829.xlsx'):
    tables = readExcel(file)
    table = [tables[1]]


def getOneSheetContext(file,sheet):
    table = getOneSheetfile(file,sheet)
    Q_id,Q,R = [],[],[]
    for i in xrange(table.nrows):
        Q_id.append(table.row_values(i)[0])
        Q.append(table.row_values(i)[1])
        R.append(table.row_values(i)[2])
    return Q_id,Q,R

def getOneSheetfile(file,sheet):
    bk = xlrd.open_workbook(file)
    table_names = bk.sheet_names()
    table = bk.sheet_by_name(sheet)
    return table

# 获取目录
def getAllFilesInDir(dirPath):
    files = [f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    # print files
    # for file in files:
    #     print  file
    return files

# 获取目录下所有文件问题句子
def getAllFilesContext(files,dirPath):
    print "Reading ... ..."
    sentences = []
    for file in files:
        if file[-4:] == '.txt':
            lines = readTXTFile(dirPath+"/"+file)
            # sentences.extend()
            if file.find("shurufa"):
                sentences.extend(lines)
            else:
                sentences.extend(preProcess.removeContext(lines))
        elif file[-5:] == '.xlsx' or file[-4:] == '.xls':
            Q_s,R_s = getFileSentence(dirPath+'/'+file)
            sentences.extend(Q_s)
        else:
            continue
    print 'Finished reading ... ...'
    return list(set(sentences))

# 获取所有的Excel file
def getAllExcelFile(files,dirPath):
    sentences = []
    for file in files:
        # print file
        if file[-5:] == '.xlsx' or file[-4:] == '.xls':
            Q_s,R_s = getFileSentence(dirPath+file)
            sentences.extend(Q_s)
    return sentences

def readStopWord(file):
    stop_words = []
    with open(file,"r") as fp:
        line = fp.readline()
        while line:
            stop_words.append(line.split('\n')[0])
            line = fp.readline()
    return stop_words

def readPunctuation(file):
    Punctuation = []
    with open(file,'r') as fp:
        line = fp.read().split('\n')[0]
        Punctuation = line.split(' ')
    return Punctuation

def getQueriesWithId(filename = 'AllQueriesWithID'):
    sentences = []
    with codecs.open(MyCode.config.QueryPath+filename+ '.txt', 'r') as fp:
        line = fp.readline()
        while line :
            items = line.strip().split("\t")
            sentences.append(items[1])
            line = fp.readline()
    return sentences


def read_souhu_fenci_file(filePath=config.CorpusFilePath,subfilename='souhu_fenci'):
    file = filePath+subfilename
    sentences = []
    for i in xrange(10):
        curfile = file + "{:02d}".format(i)+".txt"
        with codecs.open(curfile,'r',encoding='utf-8') as fp:
            line = fp.readline()
            while line :
                sentences.append(line.strip())
                line = fp.readline()

    return sentences

def ReadValueFromFile(self,file="trainData_X"):
    file = config.ModelPath+file+".model"
    model = None
    with open(file,'rb') as fp:
        try :
            model = pickle.load(fp)
        except Exception,e:
            model = None
        # finally:
        #     model = None
    return model

def getQueriesSentence(file=config.SimilarlySentencePath+"AllQueriesWithID.txt"):
    # file =
    sentences = readTXTFile(file)
    quries = []
    for sen in sentences:
        quries.append(sen.strip().split("\t")[1].replace(" ",''))
    return quries


def main():
    sentences = getQueriesSentence()
    for sen in sentences:
        print sen
    # files = getAllFilesInDir(config.CorpusFilePath)
    # sentences = getAllExcelFile(files,config.CorpusFilePath)
    # for sen in sentences:
    #     print sen
    # getQueriesWithId('AllQueriesWithID')

    # 备份
    # def filter(self,sentence):
    #     # filter the second person ralationship and Determine sentences topic as 'relationship'
    #     for i in xrange(len(sentence.words)):
    #         if u'人|关系' in sentence.words[i].word_semantic and (sentence.words[i-1].text == u'你'\
    #                 or sentence.words[i-1].text == u'你的'):
    #             sentence.topics[0] = u'relationship'
    #             break
    #
    #     return

    # self.filter(sentence)

if __name__ == '__main__':
    main()
