	# """"ranker """
	# """
     #    判断两个句子的相似度
     #    :param sentence_a,sentence_b 两个文本
     #    return disorder_degree : ？,similarly :输入文本的相似度.
	# """
	# def calcSentenceSimilarity(self,sentence_a,sentence_b):
     #    query_a_WordList = jieba.cut(sentence_a)
     #    query_b_WordList = jieba.cut(sentence_b)
     #    disorder_degree,similarly = self.calcSimilarityScoreByWordListByIdf(query_a_WordList,query_b_WordList)
     #    return disorder_degree,similarly
	#
	#
	# """TopicResponse"""
	#
	# """
	# 	获取最相似的query 基于文本相似度（计算: Engine.Ranker.Ranker）
	# 	输入:sentence 内容 text ，topic 数据， 相似度的阈值（默认值:1.0;满足阈值内的可以返回，无满足返回空）
	# """
	# def getSimilarlyQueryByRanker(self, sentence_text, topic, threshold=0.7):
	# 	simi_query = None
	# 	min_val = threshold
	#
	# 	for query in topic["query"]:
	# 		sen_text = query["text"]
	# 		disorder_degree, simi_val = self.ranker.calcSentenceSimilarity(sen_text, sentence_text)
	# 		if simi_query > min_val:
	# 			simi_query = query
	# 			min_val = simi_val
	# 	return simi_query
	#
	#
	# """
	# 	获取同意，或不同意回复时，的兜底回复。
	# 	基于文本相似度
	# 	输入：sentence 内容 text ,topic 数据，相似度阈值（默认值：0.5）
	# """
	# def getAgreeQueryByRanker(self, sentence_text, topic, threshold=0.5):
	# 	response = None
	# 	for sen in topic["agree_query"]:
	# 		disorder_degree, simi_val = self.ranker.calcSentenceSimilarity(sen, sentence_text)
	# 		if simi_val > threshold:
	# 			response = random.choice(topic["agree_response"])
	# 	if response:
	# 		return response
	#
	# 	for sen in topic["disagree_query"]:
	# 		if sen == sentence_text:
	# 			response = random.choice(topic["disagree_response"])
	# 	return response
