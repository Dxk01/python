$!/usr/bash
## _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-27
# start hadoop , hive , spark

# sudo s
#start hadoop
filePath=/home/mysql1/ 

cd $filePath/hadoop/
./sbin/start-dfs.sh
# ./sbin/start-yarn.sh

#start hive 
cd $filePath/hive/bin
source /etc/profile
hive --service metastore &
hive --service hiveserver2 &

#start spark 
cd $filePath/spark
./sbin/start-all.sh

export PATH=$PATH:/home/mysql1/spark/python
source /etc/profile

# show 
jps 
source /etc/profile
subl

