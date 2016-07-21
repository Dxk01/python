#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-06-16

import re

class chinese():
	def __init__(self):
		pass

	#判断是都包含中文
	def is_chinese(self,c_str):
		zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
		#一个小应用，判断一段文本中是否包含简体中：
		# contents=u'一个小应用，判断一段文本中是否包含简体中：'
		match = zhPattern.search(c_str)
		if match:
			an = re.compile(u'[^\u4e00-\u9fa5,^\s,\d]+')
			ma = an.search(c_str)
			if ma:
				# print ma.group(0)
				return False
		return True

	def is_english(self,word):
		if word.isalnum():
			if word.isdigit():
				return False
			else:
				return True
		return False

	#是否包含单引号
	def is_contains(self,c_str):
		an = re.compile(u'\'')
		match = an.search(c_str)
		if match:
			return True
		else:
			return False

	# judge word punctuation contaned
	def is_punctuation(self,c_str):
		an = re.compile(u'[,.:;?=%!*&()^\-+#$@~`。，、‘；】【、’|]') #   ,.:;?=-!%*&()^
		match = an.search(c_str)
		if match :
			return True
		else:
			return False
	#judge word is japanese
	def is_japanese(self,c_str):
		zhPattern = re.compile(u'[\u3040-\u30FF,\u4e00-\u9fa5,\s]+')
		# an = re.compile('')
		#一个小应用，判断一段文本中是否包含japan：
		# contents=u'一个小应用，判断一段文本中是否包含japan'
		match = zhPattern.search(c_str)
		if match:
			an = re.compile(u'[^\u3040-\u30FF,^\u4e00-\u9fa5,^\s,\d]+')
			ma = an.search(c_str)
			if ma:
				# print ma.group(0)
				return False
		return True
	#judge word is Russian
	def is_Russian(self,c_str):
		zhPattern = re.compile(u'[\u0400-\u1279,\s]+')
		# an = re.compile('')
		#一个小应用，判断一段文本中是否包含japan：
		# contents=u'一个小应用，判断一段文本中是否包含japan'
		match = zhPattern.search(c_str)
		if match:
			an = re.compile(u'[^\u0400-\u1279,^\s,^\u0000-\u007F,^\d]+')
			ma = an.search(c_str)
			if ma:
				# print ma.group(0)
				return False
		return True

	#judge word is french
	def is_French(self,c_str):
		zhPattern = re.compile(u'[\u0400-\u1279,\s]+')
		# an = re.compile('')
		#一个小应用，判断一段文本中是否包含japan：
		# contents=u'一个小应用，判断一段文本中是否包含japan'
		match = zhPattern.search(c_str)
		if match:
			an = re.compile(u'[^\u0400-\u1279,^\s,^\u0000-\u007F,^\d]+')
			ma = an.search(c_str)
			if ma:
				# print ma.group(0)
				return False
		return True

	#judge word is germen
	def is_Germen

def print_code():
	for i in xrange(1024,1279):
		print u'%c'%i,
		if (i-2) % 10 == 0 and i != 0:
			print ''

def main():
	chin = chinese()
	print_code()
	# str_1 = u'微信'
	# str_2 = u'应用fashkjhdfshajfj fhdsjkahfdhak fdsa'
	# print ('影视大全','影视大全')
	# print '360影视大全',"is",chin.is_punctuation('影xx视,.大全')
	# print str_2,"is",chin.is_chinese(str_2)
	str_japan = u'Встретились как-то Любовь и Друж'
	print str_japan
	print chin.is_Russian(str_japan)

if __name__ == '__main__':
	main()