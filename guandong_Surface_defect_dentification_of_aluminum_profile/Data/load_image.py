# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def load_image_tensorflow(filename,isFlatten=False):
    image_contents = tf.read_file(filename)   #读取文件
    image = tf.image.decode_jpeg(image_contents, channels=3)     #解码jpeg
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        img=sess.run((image))          #img为三维数组
        print (img.shape)          #输出数组形状
        print (img)                     #打印数组
        plt.imshow(img)        #显示数组
#       plt.show()
        plt.savefig("d:\\examples.jpg") #功能太强大了，可以直接将plt的图绘出到图像文件中，便于后期整理学习。
    return img,img.shape


img, shape = load_image_tensorflow("Data/guangdong_round1_train1_20180903/凸粉20180901101133对照样本.jpg")

print(shape)
