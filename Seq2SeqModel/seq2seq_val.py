# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-10-28
# 模式：train, test, serve
mode = 'train'

# 相关文件路径
BASE_PATH = "/Users/orion/PycharmProjects/Test2/Data／Seq2Seq/"
train_enc = BASE_PATH+'data/train.enc'
train_dec = BASE_PATH + "data/train.dec"
test_enc = BASE_PATH + "data/test.enc"
test_dec = BASE_PATH + "data/test.dec"

# 模型文件
work_dir = "work_dir/"

enc_vocab_size = 20000
dec_vocab_size = 20000

# 网络层数
num_layer = 3

#  每层大小， 可以取值：128， 256，512，1024 。。。。
layer_size = 128

max_train_data_size = 0

batch_size = 64

# 每多少次迭代存储一次模型
steps_per_checkpoint = 300
learning_rate = 0.5  # 学习率
learning_rate_decay_factor = 0.99  # 学习速率下降系数
max_gradient_norm = 5.0

