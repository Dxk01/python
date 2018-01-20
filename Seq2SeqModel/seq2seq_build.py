# _*_ coding:utf8 _*_
# wirter :lgy
# datetime : 2017-12-28
# function : test seq2seq

class MySeq2Seq(object):
	"""
	seq2seq model 简单实现
	与数据无关，训练时需将数据处理，配置config设置相关参数
	"""
	AVAILABLE_MODELS = ["embedding_rnn", "embedding_attention"] # 编码层网络结构类型： rnn 和 attention 等
	def __init__(self, seq2seq_model=None, verbose=None, name=None, data_dir=None):
		"""
		model init
		:param seq2seq_model: 模型类型 rnn 和 attention
		:param verbose: tensorboard 显示参数 0，1， 2， 3
		:param name: 模型名
		:param data_dir: 模型存储路径
		"""
		self.seq2seq_model = seq2seq_model
		self.verbose = verbose
		self.name = name
		self.data_dir = data_dir

	# def model(self,):
