import sys
import time
sys.path.append('..')
from dao.database import db,pymongo

def init_table():

	'''每次聚类初始化表'''
	table = db['papercluster']
	papers = table.find()
	print(papers.count())
	for paper in papers:
		table.update({'title':paper.get('title')},{'$set':{'group':'','vector':'','valid':0}})
	print('init table success!')

def init_data():

	'''聚类表数据初始化'''
	table1 = db['paper']
	papers = table1.find()
	table2 = db['papercluster']
	for paper in papers:
		content = paper.get('content')
		if content:
			keytime = find_time(content)
			keyplace = find_place(content)
			keyrole = find_role(content)
			term = find_term(content)
			keyterm = []
			keyweight = []
			for i in term:
				keyterm += [i[0]]
				keyweight += [i[1]]
			d = {
				'title':paper.get('title'),
				'url':paper.get('url'),
				'timestamp':paper.get('timestamp'),
				'keytime':keytime,
				'keyplace':keyplace,
				'keyrole':keyrole,
				'keyterm':keyterm,
				'keyweight':keyweight,
				'vector':'',
				'group':'',
				'valid':0
			}
			exist = table2.find_one({'title':paper.get('title')})
			if exist:
				print('%s paper exist!' %paper.get('title'))
			else:
				print(d)
				table2.insert(d)
				print('insert %s success!' %paper.get('title'))

def add_data():

	'''每次聚类添加新产生的数据'''
	table1 = db['paper']
	papers = table1.find().sort('timestamp',pymongo.DESCENDING).limit(1000)
	table2 = db['papercluster']
	for paper in papers:
		content = paper.get('content')
		if content:
			keytime = find_time(content)
			keyplace = find_place(content)
			keyrole = find_role(content)
			term = find_term(content)
			keyterm = []
			keyweight = []
			for i in term:
				keyterm += [i[0]]
				keyweight += [i[1]]
			d = {
				'title':paper.get('title'),
				'url':paper.get('url'),
				'timestamp':paper.get('timestamp'),
				'keytime':keytime,
				'keyplace':keyplace,
				'keyrole':keyrole,
				'keyterm':keyterm,
				'keyweight':keyweight,
				'vector':'',
				'group':'',
				'valid':0
			}
			exist = table2.find_one({'title':paper.get('title')})
			if exist:
				print('%s paper exist!' %paper.get('title'))
				break
			else:
				print(d)
				table2.insert(d)
				print('insert %s success!' %paper.get('title'))

def set_cluster_paper(date,style='DAY'):

	'''根据时间设定需要聚类的新闻'''
	startTime = int(time.mktime(time.strptime(date+' 00:00:00' ,'%Y-%m-%d %H:%M:%S')))
	#获取当前日期0点时间戳
	endTime = int(time.mktime(time.strptime(date+' 23:59:59' ,'%Y-%m-%d %H:%M:%S')))
	#获取当前日期最后时刻时间戳
	table = db['papercluster']
	if style == 'DAY':
		papers = table.find({'timestamp':{'$gt':startTime,'$lt':endTime}})
		print(papers.count())
	elif style=='WEEK':
		startTime = startTime-3600*24*6
		papers = table.find({'timestamp':{'$gt':startTime,'$lt':endTime}})
		print(papers.count())
	elif style=='ALL':
		papers = table.find()
	for paper in papers:
		table.update({'title':paper.get('title')},{'$set':{'valid':1}})
	print('set papers to cluster success!')

def init_dict():

	'''初始化聚类新闻的关键词字典'''
	table = db['papercluster']
	papers = table.find({'valid':1})
	vocabset = set([])
	for paper in papers:
		keywords = paper.get('keyterm')
		vocabset = vocabset | set(keywords)
	vocablist = list(vocabset)
	print(len(vocablist))
	return vocablist

def create_vector(vocablist):

	'''创建新闻关键词向量'''
	table = db['papercluster']
	papers = table.find({'valid':1})
	for paper in papers:
		inputset = paper.get('keyterm')
		weight = paper.get('keyweight')
		returnvec = [0]*len(vocablist)
		for word in inputset:
			if word in vocablist:
				returnvec[vocablist.index(word)] = weight[inputset.index(word)]
		table.update({'title':paper.get('title')},{'$set':{'vector':returnvec}})
		print('update %s success!' %paper.get('title'))

def save_result(clusterassment):

	'''将聚类结果保存到数据库'''
	table = db['papercluster']
	papers = table.find({'valid':1})
	for i,paper in zip(range(papers.count()),papers):
		table.update({'title':paper.get('title')},{'$set':{'group':int(clusterassment[i])}})
	print('update success!')

def run():
	#init_data()
	init_table()
	add_data()
	set_cluster_paper('2017-02-17',style='WEEK')
	vocablist = init_dict()
	create_vector(vocablist)

if __name__ == "__main__":
	run()
