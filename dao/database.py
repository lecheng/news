# -*- coding: utf-8 -*-
import pymongo
mongoCon = pymongo.MongoClient('127.0.0.1')
db = mongoCon.data
#db.authenticate('lecheng','19930324')

def get_emotions(wordname=""):

	'''获取情感词'''
	table = db['emotionaldict']
	if wordname == "":
		emotions = table.find()
	else:
		emotions = table.find_one({'wordname':wordname})
	return emotions

def save_paper(paperinfo):

	'''保存文章信息'''
	d = {
			'title': paperinfo.get('title'),
			'url': paperinfo.get('url'),
			'source': paperinfo.get('source'),
			'spider': paperinfo.get('spider'),
			'content': paperinfo.get('content'),
			'comment': paperinfo.get('comment'),
			'scan': paperinfo.get('scan'),
			'time': paperinfo.get('time'),
			'timestamp': paperinfo.get('timestamp')
	}
	table = db['paper']
	exist = table.find_one({'title':paperinfo.get('title')})
	if exist:
		print('%s paper exist!' %paperinfo.get('title'))
	else:
		print(d)
		table.insert(d)
		print('insert %s success!' %paperinfo.get('title'))