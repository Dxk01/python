# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-07

from MyCode.Algorithm.K_means import Cluster_K_means
# from SentenceSimilarly import Doc2Vec
from Doc2Vec import Doc2VecObj
from MyCode import config
from MyCode.tools import ReadFile

class SentencesClusters(object):
	def __init__(self,k_top = 200,model=None):
		self.cluster = Cluster_K_means(k_topic=k_top,model=model)
		self.sentences = None

	def getCluster(self,sentences):
		result = self.cluster.Cluster(sentences,distanceType=True)
		for index,re in enumerate(result):
			# print index
			# cluster = result[re]
			print index,"\t:\n"
			for sentence in re:
				print sentence
			print

def main():
	model = Doc2VecObj()
	model.load()
	sc = SentencesClusters(20,model)
	filename = config.SimilarlySentencePath + "AllQueriesWithID.txt"
	sentences = ReadFile.readTXTFile(filename)

	train_sentences = []
	for sen in sentences:
		sen_iterms = sen.split("\t")
		# print sen_iterms[1]
		if len(sen_iterms) >= 2:
			# print sen_iterms[1].strip().replace(" ","")
			train_sentences.append(sen_iterms[1].strip().replace(" ", ""))

	sc.getCluster(train_sentences[:100])

if __name__ == '__main__':
	main()
