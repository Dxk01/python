# -*- coding: utf-8 -*-

# Write : lgy
# Data : 2017-09-24
# function: Algorithm class Connections for bp network

class Connections(object):
	def __init__(self):
		self.connections = []

	def add_connection(self, connecton):
		self.connections.append(connecton)

	def dump(self):
		for conn in self.connections:
			print conn