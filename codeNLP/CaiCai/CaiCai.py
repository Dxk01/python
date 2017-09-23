# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-15

import os
import time

import jieba

import MyCode.config
from MyCode.tools import ReadFile


# 处理临时Excel 文件
def getQRsentences(file=MyCode.config.CaiCaiPath + "0812caicai.xlsx"):
    tables = ReadFile.readExcel(file)
    Q_R_sentences = []
    for table in tables:
        for i in xrange(1,table.nrows):
            lines = table.row_values(i)[0:]
            values = []
            for va in lines:
                values.append(va)
            # print values
            Q_R_sentences.append(values)
    # Q_par(Q_R_sentences)
    print len(Q_R_sentences)
    return Q_R_sentences

# 问题分词
def Q_par(Q_R_sentences):
    for sen in Q_R_sentences:
        words = jieba.cut(sen[1])
        line = ''
        for w in words:
            line += w + ' '
        line = line[:-1]
        sen[1] = line

#   获取Ques sentences
def getQuestionFile(Q_R_sentences):
    QIdfile = MyCode.config.CaiCaiDataPath + "AllQueriesWithID.txt"
    QnIdfile = MyCode.config.CaiCaiPath + "AllQueriesWithID.txt"
    mapQRfile = MyCode.config.CaiCaiDataPath + "AllQueryResponseIdMap.txt"
    mapnQRfile = MyCode.config.CaiCaiPath + "AllQueryResponseIdMap.txt"
    RIdfile = MyCode.config.CaiCaiDataPath + "AllResponsesWithID.txt"
    RnIdfile = MyCode.config.CaiCaiPath + "AllResponsesWithID.txt"

    Q_sentences = ReadFile.readTXTFile(QIdfile)
    QR_map = []
    OldMapQid = {}
    MapRId = {}
    MapQid = {}
    r_id = 1
    q_id = 1
    OldRIdSentences = ReadFile.readTXTFile(RIdfile)
    R_sens = []
    for line in OldRIdSentences:
        R_sens.append(line.strip().split("\t")[1])

    R_sens = list(set(R_sens))

    for qr_sentence in Q_R_sentences:
        csentence = []
        exist = False
        for sentence in Q_sentences:
            csentence = sentence.strip().split('\t')
            line = csentence[1].replace(' ','')
            if line == qr_sentence[0]:
                exist = True
                break
        if exist:
            sq_id = csentence[0]
            OldMapQid.setdefault(sq_id,'')
        else:
            sq_id = "CAICAI_Q_"+str(time.strftime("%Y%m%d%H%M", time.localtime()))+"%05d"%q_id
            q_id += 1
            MapQid.setdefault(sq_id,qr_sentence[1].replace(' ',''))
        for i in xrange(2, 5):
            if qr_sentence[i] in R_sens:
                continue
            if qr_sentence[i] != '' and len(qr_sentence[i]) > 2:
                print qr_sentence[i]
                sr_id = 'CAICAI_R_'+str(time.strftime("%Y%m%d%H%M", time.localtime()))+'%05d' % r_id
                QR_map.append((sq_id, sr_id))
                MapRId.setdefault(sr_id,qr_sentence[i])
                r_id += 1

    fileEnd = MyCode.config.CaiCaiPath + 'AllQueriesWithIDfinished.txt'
    # 重写Questions 文件
    with open(fileEnd,'w') as fp:
        # print len(OldMapQid.keys())
        for sen in Q_sentences:
            lines = sen.split('\t')[0]
            if OldMapQid.has_key(lines):
                fp.write(sen[:-2]+',"client_id": "c_00000007"}\n')
            else:
                fp.write(sen)
    # 结果写入文件
    with open(QnIdfile,'w') as fp:
        MapQid = sorted(MapQid.iteritems(),key=lambda asd:asd[0],reverse=False)
        for id in  MapQid:
            fp.write(id[0]+'\t'+id[1]+"\n")
    with open(mapnQRfile,'w') as fp:
        sen = ReadFile.readTXTFile(mapQRfile)
        for s in sen:
            lines = s.split('\t')
            print lines
            QR_map.append((lines[0],lines[1][:-1]))
        QR_map = list(set(QR_map))
        for qr in sorted(QR_map,key=lambda asd:asd[0],reverse=False):
            fp.write(qr[0]+'\t'+qr[1]+'\n')

    with open(RnIdfile,'w') as fp:
        MapRId = sorted(MapRId.iteritems(),key=lambda asd:asd[0],reverse=False)
        for id in MapRId:
            fp.write(id[0]+'\t'+id[1].strip()+'\t{"client_id": "c_00000007"}\n')

def execOrder(orders):
    for order in orders:
        print order
        print os.system(order)
        # time.sleep(10)


# 插入 相关字典项
def insertDicItem():
    file = MyCode.config.CaiCaiPath + 'AllQueriesWithID_mid2.txt'
    fileEnd = MyCode.config.CaiCaiPath + 'AllQueriesWithIDfinished.txt'
    sentences = ReadFile.readTXTFile(file)
    with open(fileEnd,'a+') as fp:
        for sen in sentences:
            lines = sen.split("\t")
            lines[2] = lines[2][:-3]+', "client_id": "c_00000007"}'
            # print lines[2]
            fp.write(lines[0] +"\t"+lines[1]+'\t'+lines[2]+'\n')


def main():
    """
        # caicai 语料
        # 首先 运行ReadFile前两函数 注释其他内容 中采采获取三个文件，
        # 运行 海哥脚本 处理句子成分分析
        # 运行 第三个函数 注释其他
        #
        # 最后将结果 copy到工程下，更新索引文件
        # chat——system／tools/dev/query_tools/下脚本，根据说明配置运行

        """
    senyences = getQRsentences(MyCode.config.CaiCaiPath + "0812caicai.xlsx")
    for sen in senyences:
        print sen
    getQuestionFile(senyences)
    execOrder(['python /Users/orion/lgy/chat_system/tools/dev/script_tools/segment_script.py \
    %s %s %s' % (
    MyCode.config.CaiCaiPath + "AllQueriesWithID.txt", MyCode.config.CaiCaiPath + "AllQueriesWithID_mid1.txt",
    MyCode.config.CaiCaiPath + "result.log.txt"),\
               'python /Users/orion/lgy/chat_system/tools/dev/script_tools/label_domain.py \
               %s %s %s' % (MyCode.config.CaiCaiPath + "AllQueriesWithID_mid1.txt",
                            MyCode.config.CaiCaiPath + "AllQueriesWithID_mid2.txt",
                            MyCode.config.CaiCaiPath + "report.AllQueriesWithID.txt")])
    insertDicItem()

if __name__ == '__main__':
    main()