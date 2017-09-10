# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-29

# function  语料处理成数据

import  sys
sys.path.append('../..')
reload(sys)
from MyCode.tools import ReadFile
import numpy
import  lda
import pickle
from MyCode import config
import logging
import gensim