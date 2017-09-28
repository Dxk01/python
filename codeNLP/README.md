Introduce


该 code 主要是工作学习之余，个人学习实践的部分代码
主要包括
Algorthm : 学习工作中使用的相关算法的学习和实现
    gensim下的LDA ，HDA  用于主题分析
    K_mean实现，主要处理文本，词的聚类问题
    Perceptron : 个人学习的感知器算法实现
    LinearUnit : 线性单元实现，即继承Perceptron

AnalysisText : 主要涉及文本分词和词标记
    主要是通过jieba,thulac,nltk 相关标记库，标记文本词，并实验对比三种标记的性能，精确度
    
SentenceSimilarly : 主要涉及句子的相似度问题，解决query 泛化和同义句匹配问题
    实现了 doc2vec (paragraph2vec based word2vec),docsim (sentence2vec),jecard distance combine tf-idf 
    
Spider : 引用网上的微博评论爬取的code
		Login.py 知乎模拟登陆脚本，还有验证码识别脚本，但因准确率问题，在调试中
		SpiderTopicData.py 爬取知乎topic 数据，以及topic 树关系
		SpiderTopicQuestions.py 爬取topic 下的questions 数据，开发中 。。。 。。。
		


tools ： pre process scripts


config.py  : code file path configure

MyTest.py : for test 


