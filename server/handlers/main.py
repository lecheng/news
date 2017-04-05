import tornado.web
import sys
import json
sys.path.append('..')
from dao.visual import cluster_result

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		data = cluster_result()
		self.render('graph.html',data=data)
	pass