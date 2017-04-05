# -*- coding: utf-8 -*-
import sys
import jieba
import jieba.posseg as posseg
import jieba.analyse
sys.path.append('..')

from dao.database import *
from dao.dictdao import save_emotionaldict

def load_emotionaldict():
	table = db['emotionaldict']
	if(not table.count()):
		save_emotionaldict()

def emotion(content):

	'''获取内容的情感'''
	#list为二维列表，第一维存词名，第二维存对应词频
	load_emotionaldict()
	l = [[],[]]
	item = {}

	validate = ['n','nl','v','vd','vf','vx','vi','vl','vg','a','ad','an','ag','al','d','p']
	happy = ['PA','PE']
	item['乐'] = 0
	#乐
	good = ['PD','PH','PG','PB','PK']
	item['好'] = 0
	#好
	angry = ['NA']
	item['怒'] = 0
	#怒
	sad = ['NB','NJ','NH','PF']
	item['哀'] = 0
	#哀
	afraid = ['NI','NC','NG']
	item['惧'] = 0
	#惧
	bad = ['NE','ND','NN','NK','NL']
	item['恶'] = 0
	#恶
	surprise = ['PC']
	item['惊'] = 0
	#惊
	item['中性'] = 0
	#中性：0
	item['褒义'] = 0
	#褒义：1
	item['贬义'] = 0
	#贬义：2
	both = 0
	#兼有褒贬：3
	words = posseg.cut(content)
	for word in words:
		if word.flag in validate:
			if word.word not in l[0]:
				l[0] += [word.word]
				l[1] += [1]
			else:
				l[1][l[0].index(word.word)] += 1
	for i in l[0]:
		emotion = get_emotions(i)
		if emotion: 
			first_emotion = emotion.get('first_emotion')
			#获取主情感词
			first_strength = emotion.get('first_strength')
			#获取主情感词强度
			number = l[1][l[0].index(i)]
			#获取词频
			if first_emotion in happy:
				item['乐'] = item.get('乐') + int(first_strength)*number
			elif first_emotion in good:
				item['好'] = item.get('好') + int(first_strength)*number
			elif first_emotion in angry:
				item['怒'] = item.get('怒') + int(first_strength)*number
			elif first_emotion in sad:
				item['哀'] = item.get('哀') + int(first_strength)*number
			elif first_emotion in afraid:
				item['惧'] = item.get('惧') + int(first_strength)*number
			elif first_emotion in bad:
				item['恶'] = item.get('恶') + int(first_strength)*number
			elif first_emotion in surprise:
				item['惊'] = item.get('惊') + int(first_strength)*number
			first_appraise = emotion.get('first_appraise')
			if  first_appraise == "0":
				item['中性'] = item.get('中性') + int(first_strength)*number
			elif first_appraise == "1":
				item['褒义'] = item.get('褒义') + int(first_strength)*number
			elif first_appraise == "2":
				item['贬义'] = item.get('贬义') + int(first_strength)*number
			elif first_appraise == "3":
				item['褒义'] = item.get('褒义') + int(first_strength)*number
				item['贬义'] = item.get('贬义') + int(first_strength)*number
	print(item)
	return item

def run():
	f = open('../file/sample/sample1.txt','r',encoding='utf-8')
	content = f.read()
	emotion(content)
	f.close()

if __name__ == "__main__":
	run()

