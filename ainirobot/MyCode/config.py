import sys
import os
sys.path.append('.')
sys.path.append("..")
sys.path.append("Algorithm/")
sys.path.append("shellTools/")

# ProcessBaseFilePath = "/home/hongkeyuan/lgy/Test2/"
ProcessBaseFilePath = "/Users/orion/PycharmProjects/Test2/"
ChatSystemPath = "/Users/orion/PycharmProjects/Chat/chat_system/chatter/"
ResultFilePath = ProcessBaseFilePath+'Data/Result/'
RegularsFilePath = ChatSystemPath+'Data/Common/Regulars/'
InputDataFilePath = ProcessBaseFilePath+'Data/'
CodeFile = ProcessBaseFilePath+"MyCode"
AlgorithmPath = CodeFile + 'Algorithm'

chatSystemDataPath = ChatSystemPath+"Data/"
# chatSystemDataPath =
chatSystemDataPath2 = "/Users/orion/PycharmProjects/Chat/chat_system/chatter.v2/Data/"
chat2Semantic_dicPath = "/Users/orion/PycharmProjects/Chat/chat_system/chatter.v2/Data/Language/zh-CN/Dictionary/Semantic_dic/"

DataFilePath = ProcessBaseFilePath+'Data/'
BadCaceFilePath = DataFilePath+"badcase/"
ConfigFilePath = DataFilePath+'Config/'
CorpusFilePath = DataFilePath+'corpus/'
MidResultPath = DataFilePath + 'Mid_result/'
ResultPath = DataFilePath + 'Result/'
StopWordPath = DataFilePath + 'StopWords/'
temdealData = DataFilePath + 'CaiCaiData/'
WordDicPath = DataFilePath + "Worddic/"
ModelPath = ResultFilePath + 'Model/'
QueryPath = DataFilePath + 'Query/'
CaiCaiPath = DataFilePath + 'CaiCaiData/'
XiaoYaDataPath = chatSystemDataPath + "XiaoYa/"
CaiCaiDataPath = XiaoYaDataPath+"CaiCai/"
Semantic_dicPath = chatSystemDataPath+"Language/zh-CN/semantic_dic/"
WordClusterPath = DataFilePath+"Result/WordCluster/"
SentenceKeyWordPath = DataFilePath+"SentenceKeyWordFile/"
SimilarlySentencePath = DataFilePath + "SimilarlySentence/"
QueryTestPath = DataFilePath+"QueryTestResult/"
TopicFilePath = DataFilePath + "Topic/"

# value globle
key = '1UGV9593A703DCZ5'

link_url = 'http://localhost:8000/helloaini/?key=' + key + '&q='

