Introduce


该 code 主要是工作学习之余，个人学习实践的部分代码
主要包括
Algorthm : 学习工作中使用的相关算法的学习和实现
    gensim下的LDA ，HDA  用于主题分析
    K_mean实现，主要处理文本，词的聚类问题
    Perceptron : 个人学习的感知器算法实现
    LinearUnit : 线性单元实现，即继承Perceptron
    NeuralNetwork : 神经网络基础算法实现
    TopicModel ：主题分析相关算法实现，包括 LDA，HDA（使用gensim 包实现），以及在short text 话题分析中表现较好的BTM（Biterm Topic Model）等分析模型
    参考文献：
        A Biterm Topic Model for Short Texts
        Xiaohui Yan, Jiafeng Guo, Yanyan Lan, Xueqi Cheng
        Institute of Computing Technology, CAS
        Beijing, China 100190 yanxiaohui@software.ict.ac.cn, {guojiafeng, lanyanyan, cxq}@ict.ac.cn
        coding C++ ：BTM: https://github.com/xiaohuiyan/BTM
                     online BTM: https://github.com/xiaohuiyan/OnlineBTM
                     bursty BTM: https://github.com/xiaohuiyan/BurstyBTM 
    其中 burstyBTM 尚未实现，后续追加。。。。。


AnalysisText : 主要涉及文本分词和词标记
    主要是通过jieba,thulac,nltk 相关标记库，标记文本词，并实验对比三种标记的性能，精确度
    
SentenceSimilarly : 主要涉及句子的相似度问题，解决query 泛化和同义句匹配问题
    实现了 doc2vec (paragraph2vec based word2vec),docsim (sentence2vec),jecard distance combine tf-idf 
    
Spider : 引用网上的微博评论爬取的code
		Login.py 知乎模拟登陆脚本，还有验证码识别脚本，但因准确率问题，在调试中
		SpiderTopicData.py 爬取知乎topic 数据，以及topic 树关系
		SpiderTopicQuestions.py 爬取topic 下的questions 数据，可以配置获取question 的数量，存储位置
        SpiderData.py 爬取 批量 topic的批量问题，需要设置topic SpiderTopicData 爬取的数据topic——link数据解析出叶子话题，code中时获取从根话题算起的第三级话题
        TopicTree.py 有根据SpiderTopicData.py爬取的topic数据构建话题树
        注：话题中未必话题爬取时的封号或封IP问题采用随机定时间隔爬取连接的方法，效率可能有点慢，可根据需要修改；
        为保险起见最好保留，以避免封号或封IP的问题
		


tools ： pre process scripts


config.py  : code file path configure

MyTest.py : for test 


