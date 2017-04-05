import sys
sys.path.append('..')
from analysis.emotion_analysis import emotion
from analysis.keyword_analysis import keywords
from dao.database import db

def cluster_result():

	'''获取聚类结果数据'''
	table = db['papercluster']
	papers = table.find({'valid':1})
	group = []
	data = {}
	nodes = []
	links = []
	for paper in papers:
		if paper.get('group') not in group:
			group += [paper.get('group')]
			tempnode = {
				'name':('group'+str(paper.get('group'))),
				'value':0.5,
				'group':paper.get('group'),
				'href':('show?group='+str(paper.get('group')))
			}
			nodes += [tempnode]
		tempnode = {
			'name':paper.get('title'),
			'value':1,
			'group':paper.get('group'),
			'href':('details?title='+str(paper.get('title')))
		}
		nodes += [tempnode]
		templink = {
			'source':('group'+str(paper.get('group'))),
			'target':paper.get('title'),
			'value':0.5
		}
		links += [templink]
	data['nodes'] = nodes
	data['links'] = links
	return data

def get_group_words(group,top=10):

	'''获取聚类结果群中关键词数据'''
	table = db['papercluster']
	papers = table.find({'group':int(group)})
	print(papers.count())
	data = []
	dataset = []
	for paper in papers:
		keywords = paper.get('keyterm')
		dataset += keywords
	word_count = [[],[]]
	for i,index in zip(dataset,range(len(dataset))):
		if i not in word_count[0]:
			word_count[0] += [i]
			word_count[1] += [1]
		else:
			word_count[1][word_count[0].index(i)] += 1
	for i in range(len(word_count[0])):
		d = {
			'text':word_count[0][i],
			'value':word_count[1][i],
			'url':('http://www.baidu.com/s?wd='+word_count[0][i])
		}
		data += [d]
	data = sorted(data,key=lambda result:result.get('value'),reverse=True)
	data = data[:top]
	print(data)
	return data

def get_details(title):

	'''获得新闻的详细信息'''
	table = db['paper']
	paper = table.find_one({'title':title})
	content = paper.get('content')
	emotions = emotion(content)
	keyword = keywords(content)
	pie_data = [
		{
			'name':'褒义',
			'value':int(emotions.get('褒义'))
		},
		{
			'name':'贬义',
			'value':int(emotions.get('贬义'))
		}
	]
	radar_data = [
		{
			'name':'情感值',
			'data':[
				{'axis':'好','value':emotions.get('好')},
				{'axis':'乐','value':emotions.get('乐')},
				{'axis':'哀','value':emotions.get('哀')},
				{'axis':'惊','value':emotions.get('惊')},
				{'axis':'恶','value':emotions.get('恶')},
				{'axis':'怒','value':emotions.get('怒')},
				{'axis':'惧','value':emotions.get('惧')}
			]
		}
	]
	return pie_data,radar_data,content
