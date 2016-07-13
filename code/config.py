#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-12
#，软件系统全局变量 ------ 变量声明

#

Host_IP = '127.0.0.1'
database = 'mysql_anqu_en'
dataBase_port = 3306
dataBase_user = 'root'
dataBase_passwd = 'root'

#系统运行各模块包路径
fileRootPath = '/home/spark/anqu/python/code/'
fileToolsPath = "/home/spark/anqu/python/code/Tools"
fileWordsPath = fileRootPath+'Word'
fileAnalysisPath = fileRootPath+'analysis'
fileDataPath = fileRootPath + 'data_deal'
fileClusterPath = fileRootPath + 'Cluster'

#系统运行，以来包路径配置
import sys
sys.path.append(fileRootPath)
sys.path.append(fileDataPath)
sys.path.append(fileAnalysisPath)
sys.path.append(fileWordsPath)
sys.path.append(fileRootPath+'wordAnalysis')
sys.path.append(fileToolsPath)
sys.path.append(fileClusterPath)
reload(sys)
sys.setdefaultencoding('utf8') 

