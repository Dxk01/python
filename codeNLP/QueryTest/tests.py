# coding:utf-8
from django.test import TestCase

import urllib
import urllib2
import unittest
import codecs
import json
import re
import time
import threading
import sys
import os
import datetime
from MyCode import config

key = '1UGV9593A703DCZ5'

url = 'http://localhost:8000/helloaini/?key=' + key + '&q='
# url = 'http://10.102.3.47:8000/helloaini/?key=' + key + '&q='

# in_file = "C:\Users\yulong\chat_system\chatter\Data\XiaoYa/AllQueriesWithID.txt"
test_name = 'test'
in_file = config.QueryTestPath+"{0}.txt".format(test_name)
out_file = config.QueryTestPath+"{0}_reult.txt".format(test_name)


def do_test(id, query, fp):
    print("%s : %s" % (id,query))
    try:
        start = datetime.datetime.now()
        

        req = urllib2.Request(url + urllib2.quote(query.encode('utf-8')))
        res_data = urllib2.urlopen(req)
        res = res_data.read()

        obj = json.loads(res)

        if True:
            hit_query = ''
            intent = ''
            if 'desc' in obj and 'textOutputDetail' in obj['desc'] and obj['desc']['textOutputDetail']:
                if 'hitQuery' in obj['desc']['textOutputDetail']:
                    hit_query = obj['desc']['textOutputDetail']['hitQuery']
                if 'intent' in obj['desc']['textOutputDetail']:
                    intent = obj['desc']['textOutputDetail']['intent']
            fp.write("%s\t%s\t%s\t%s\t%s\r\n" % (id, query, obj['answer']['text'], intent, hit_query))
            # fp.write("%s\t%s\t%s\r\n" % (id, query, obj['answer']['text']))
    except Exception as e:
        fp.write("%s\t%s\t%s\r\n" % (id, query, e.message))
        print e.message


# Create your tests here.
class ChatterTest(TestCase):
    threads = []
    threads_pool = []
    threads_pool_length = 1

    with codecs.open(out_file, 'w', 'utf-8') as fo:
        with codecs.open(in_file, 'r', 'utf-8') as fp:
            lines = fp.readlines()

            for line in lines:
                parts = line.strip()

                query = parts.strip().split("\t")
                if len(query) != 2:
                    continue
                id = query[0]
                th = threading.Thread(target=do_test, args=(id, query[1], fo))
                threads.append(th)

            while len(threads) > 0:
                if len(threads_pool) < threads_pool_length:
                    th = threads.pop()
                    threads_pool.append(th)
                    th.start()
                else:
                    th = threads_pool.pop(0)
                    th.join()

            if len(threads_pool) > 0:
                for th in threads_pool:
                    th.join()




if __name__ == '__main__':
    unittest.main()
