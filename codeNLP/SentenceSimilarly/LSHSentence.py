# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-08-30

# funcation 处理queries 相似度问题 文档向量（在此表示句子向量）
import sys
sys.path.append("../..")
reload(sys)
from gensim import corpora
from gensim.similarities import Similarity
import jieba
from MyCode.tools import ReadFile
from MyCode import config
from MyCode.Algorithm import LDA_Topic
from gensim.models import Doc2Vec
# from gensim.models.doc2vec import TaggedDocument
from gensim.models import TfidfModel
# from gensim.sklearn_integration import T
from sklearn.feature_extraction.text import TfidfVectorizer

raw_documents = [
	'0无偿居间介绍买卖毒品的行为应如何定性',
	'1吸毒男动态持有大量毒品的行为该如何认定',
	'2如何区分是非法种植毒品原植物罪还是非法制造毒品罪',
	'3为毒贩贩卖毒品提供帮助构成贩卖毒品罪',
	'4将自己吸食的毒品原价转让给朋友吸食的行为该如何认定',
	'5为获报酬帮人购买毒品的行为该如何认定',
	'6毒贩出狱后再次够买毒品途中被抓的行为认定',
	'7虚夸毒品功效劝人吸食毒品的行为该如何认定',
	'8妻子下落不明丈夫又与他人登记结婚是否为无效婚姻',
	'9一方未签字办理的结婚登记是否有效',
	'10夫妻双方1990年按农村习俗举办婚礼没有结婚证 一方可否起诉离婚',
	'11结婚前对方父母出资购买的住房写我们二人的名字有效吗',
	'12身份证被别人冒用无法登记结婚怎么办？',
	'13同居后又与他人登记结婚是否构成重婚罪',
	'14未办登记只举办结婚仪式可起诉离婚吗',
	'15同居多年未办理结婚登记，是否可以向法院起诉要求离婚'
]

tfidf_vectorizer = TfidfVectorizer(min_df=3, max_features=None, ngram_range=(1, 2), use_idf=1, smooth_idf=1,sublinear_tf=1)
train_documents = []
for item_text in raw_documents:
	# print(item_text)
	item_str = list(jieba.cut(item_text))
	train_documents.append(item_str)
x_train = tfidf_vectorizer.fit_transform(train_documents)

test_data_1 = '你好，我想问一下我想离婚他不想离，孩子他说不要，是六个月就自动生效离婚'
test_cut_raw_1 = list(jieba.cut(test_data_1))
x_test = tfidf_vectorizer.transform([test_cut_raw_1])

lshf = LSHForest(random_state=42)
lshf.fit(x_train.toarray())

distances, indices = lshf.kneighbors(x_test.toarray(), n_neighbors=3)
print(distances)
print(indices)

# class LSAObj(object):
# 	def __init__(self):
# 		self.model = None
# 		self.