import tornado.web
import sys
import json
sys.path.append('..')
from dao.visual import get_group_words,get_details

class ClusterVisualHandler(tornado.web.RequestHandler):
	def get(self):
		group = self.get_argument('group')
		data = get_group_words(group)
		self.render('wordcloud.html',data=data)
	pass

class DetailsVisualHandler(tornado.web.RequestHandler):
	def get(self):
		title = self.get_argument('title')
		data1,data2,content = get_details(title)
		self.render('pie.html',pie_data=data1,radar_data=data2,content=content)
		pass