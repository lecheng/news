# -*- coding: utf-8 -*-
class Emotion:
	def __init__(self):
		self.wordname = ""
		self.wordtype = ""
		self.number = ""
		self.index = ""
		self.first_emotion = ""
		self.first_strength = ""
		self.first_appraise = ""
		self.second_emotion = ""
		self.second_strength = ""
		self.second_appraise = ""

	def __str__(self):
		s = ""
		s = s + "wordname: " + self.wordname
		s = s + "wordtype: " + self.wordtype
		s = s + "number: " + self.number
		s = s + "index: " + self.index
		s = s + "first_emotion" + self.first_emotion
		s = s + "first_strength" + self.first_strength
		s = s + "first_appraise" + self.first_appraise
		s = s + "second_emotion" + self.second_emotion
		s = s + "second_strength" + self.second_strength
		s = s + "second_appraise" + self.second_appraise  
