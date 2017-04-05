# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from dao.database import db 


def save_emotionaldict():

	'''将情感词库保存到数据库中'''
	table = db['emotionaldict']
	f = open('../file/dict/emotionaldict.txt','r',encoding='utf-8')
	lines = f.readlines()
	for line in lines:
		d = {}
		s = line.split('\t')
		print(s)
		d['wordname'] = s[0]
		d['wordtype'] = s[1]
		d['number'] = s[2]
		d['index'] = s[3]
		d['first_emotion'] = s[4]
		d['first_strength'] = s[5]
		d['first_appraise'] = s[6]
		d['second_emotion'] = s[7]
		d['second_strength'] = s[8]
		d['second_appraise'] = s[9]
		exist = table.find_one({'wordname':d['wordname']})
		if exist:
			table.update({'wordname':d['wordname']},d)
			print('word %s exist and update success!' %d['wordname'])
		else:
			table.insert(d)
			print('insert %s success!' %d['wordname'])

def save_stockdict():

	'''将股票词库保存到数据库中'''
	table = db['stockdict']
	f = open('../file/dict/stockdict.txt','r',encoding='utf-8')
	lines = f.readlines()
	for line in lines:
		d = {}
		s = line.split(' ')
		stock_name = s[0]
		stock_code = s[1].replace('\n','')
		d['stockname'] = stock_name
		d['stockcode'] = stock_code
		exist = table.find_one({'stockname':stock_name})
		if exist:
			table.update({'stockname':stock_name},d)
			print('stock %s exist and update success!' %stock_name)
		else:
			table.insert(d)
			print('insert %s success!' %stock_name)


