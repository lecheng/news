import pymongo
mongoCon = pymongo.MongoClient('127.0.0.1')
db = mongoCon.data

def get_emotions(wordname=""):

	'''获取情感词'''
	table = db['emotionaldict']
	if wordname == "":
		emotions = table.find()
	else:
		emotions = table.find_one({'wordname':wordname})
	return emotions

