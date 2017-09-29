# encoding: utf-8
"""
作者：liguoyu
"""
import json
from MyCode import config
import codecs

class TreeNode(object):
	""" struct tree node"""
	def __init__(self,topic_id):
		self.cur_id = topic_id
		self.child_id_list = None
		self.parent_id_list = None

	def setCurId(self,topic_id):
		self.cur_id = topic_id

	def addChildId(self,topic_id):
		if not self.child_id_list:
			self.child_id_list = []
		if topic_id not in self.child_id_list:
			self.child_id_list.append(topic_id)

	def addParentId(self,topic_id):
		if not self.parent_id_list:
			self.parent_id_list = []
		if topic_id not in self.parent_id_list:
			self.parent_id_list.append(topic_id)

	def isLeaf(self):
		if self.child_id_list:
			return False
		else:
			return True

	def isRoot(self):
		if self.parent_id_list:
			return False
		else:
			return True

class Node(object):
	""" node struct"""
	def __init__(self):
		self.parents = None
		self.childs = None

	def addChild(self,Node):
		if not self.childs:
			self.childs = list()
		self.childs.append(Node)

	def addParent(self,Node):
		if not self.parents:
			self.parents = list()
		self.parents.append(Node)


class TopicTree(object):
	"""
	topic tree describe topic assoisation
	"""
	def __init__(self):
		"""
		初始化相关树参数
		"""
		self.treeNode = {}

	def load(self,file = config.TopicFilePath+'zhihu_topic_link_1.json'):
		with codecs.open(file,'r',encoding='utf8') as fp:
			return json.load(fp)

	def paserData(self,data):
		for key in data:
			value = data[key]
			if key not in self.treeNode:
				self.treeNode[key] = TreeNode(key)
			self.treeNode[key].addParentId(value)
			for va in value:
				if va not in self.treeNode:
					self.treeNode[va] = TreeNode(value)
				self.treeNode[va].addChildId(key)

	def getDeepTopic(self):
		topics = self.treeNode['19778317'].child_id_list
		result = []
		for topic in topics:
			result.extend(self.treeNode[topic].child_id_list)
		result = list(set(result))
		return result


	def showLeafNode(self):
		leafNodeId = []
		for node in self.treeNode:
			leafNode = self.treeNode[node]
			if leafNode.isLeaf():
				leafNodeId.append(leafNode.cur_id)
			if leafNode.isRoot():
				print "根节点ID:{}".format(leafNode.cur_id)
		print "{}叶子节点包括:\n".format(len(leafNodeId))
		for id in xrange(len(leafNodeId)):
			print leafNodeId[id],
			if id % 5 != 0 or id == 0:
				print ',',
			else:
				print ''

def main():
	topictree = TopicTree()
	data = topictree.load()
	topictree.paserData(data)
	topictree.showLeafNode()
	result = topictree.getDeepTopic()

	print "\n三级话题共有{}个，包括：\n".format(len(result))
	for id in xrange(len(result)):
		print result[id],
		if id % 5 != 0 or id == 0:
			print ',',
		else:
			print ''

if __name__ == '__main__':
	main()

