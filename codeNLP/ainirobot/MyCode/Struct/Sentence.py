# -*- coding: utf-8 -*-
# writer : lgy
# data : 2017-09-09

class Sentence(object):
	""" Class Sentence """

	def __init__(self):
		self.text = None
		self.text_type = None
		self.fragment = None
		self.words = list()

		# Primary sentence type: 0: decl; 1: ynq; 2: whq; 3: impe; 4: excl
		self.sentenceType = 0
		self.isNegative = False
		self.tense = None
		self.role = -1  # Not determined yet
		self.topics = []

		# Text Analysis: Dictionary
		self.inquiryParsingData = None

		# Intent Analysis: Dictionary
		self.intent_analysis = None

		# Emotion Analysis: Dictionary
		self.emotion_analysis = None
		return

	@staticmethod
	def create_sentence(text, text_type):
		sent = Sentence()
		sent.text = text
		sent.text_type = text_type
		return sent

	@staticmethod
	def build_words(sentence):

		if not sentence.inquiryParsingData:
			return None

		ta_wordlist = sentence.inquiryParsingData['wordlist']
		ta_word_index = 0

		words = []
		while ta_word_index < len(ta_wordlist):
			word = Word()
			word.sentence = sentence

			word.text = ta_wordlist[ta_word_index]
			word.wordType = 0  # 'Normal'
			if word.text in LingConstDef.FullWidthPunctuationList or word.text in LingConstDef.HalfWidthPunctuationList:
				word.wordType = 1  # 'Punctuation'

			words.append(word)
			ta_word_index += 1

		# if parsing is available, import rich information
		if 'stanfordNlpAnalysis' in sentence.inquiryParsingData:
			stanfordNlpAnalysisResult = sentence.inquiryParsingData['stanfordNlpAnalysis']
			parsingItems = stanfordNlpAnalysisResult['parsingItems']
			# Assumption: There is only one parsing item
			# If the assumption is wrong, we need to check sentence seperator

			parsingItem = parsingItems[0]
			utterance = parsingItem.Utterance

			ta_word_index = 0
			parsing_item_index = 0
			ta_offset = 0
			parsing_offset = 0

			parsing_uttr_word_index = 0

			while ta_word_index < len(words) and parsing_uttr_word_index < len(utterance.words):
				ta_word = words[ta_word_index]
				parsing_uttr_word = utterance.words[parsing_uttr_word_index]

				if ta_offset + len(words[ta_word_index].text) > parsing_offset + len(parsing_uttr_word.Text):
					parsing_offset += len(parsing_uttr_word.Text)
					parsing_uttr_word_index += 1
				elif ta_offset + len(words[ta_word_index].text) < parsing_offset + len(parsing_uttr_word.Text):
					ta_offset += len(words[ta_word_index].text)
					ta_word_index += 1
				else:
					# Now achieve a matching point
					if ta_offset == parsing_offset:
						# Copy Part-of-Speech
						ta_word.partOfSpeech = parsing_uttr_word.PartOfSpeech

						if parsing_uttr_word.NamedEntityTag != "O":
							ta_word.namedEntityTag = parsing_uttr_word.NamedEntityTag
							ta_word.namedEntityOffset = ta_offset

					ta_offset += len(words[ta_word_index].text)
					parsing_offset += len(parsing_uttr_word.Text)
					ta_word_index += 1
					parsing_uttr_word_index += 1

		return words

	def getWordNumber(self):
		return len(self.words)

	def getFirstWord(self):
		word = None
		if len(self.words) > 0:
			word = self.words[0]

		return word

	def getLastWord(self):
		word = None
		numOfWords = len(self.words)
		if numOfWords > 0:
			word = self.words[numOfWords - 1]

		return word

	def getSentenceType(self):
		return self.sentenceType

	def appendWord(self, word):
		self.words.append(word)
		return

	def buildHierarchy(self):
		# firstly, build link among words
		numOfWords = len(self.words)
		if numOfWords > 1:
			i = 0;
			while i < numOfWords - 1:
				self.words[i].next = self.words[i + 1]
				i += 1

			i = numOfWords - 1;
			while i > 0:
				self.words[i].prev = self.words[i - 1]
				i -= 1
		return
