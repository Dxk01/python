# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-10-02

from keras.layers import Dense, Activation
from keras.models import Sequential

class LstmObj(object):
	""" LSTM 处理时序类问题"""

	def __init__(self):
		self.model = Sequential()
		self.model.add(Dense(32, activation='relu', input_dim=7))
		self.model.add(Dense(10, activation='softmax'))
		self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

	def load(self,file):
		pass

	# def