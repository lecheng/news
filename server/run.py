import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
from handlers.main import MainHandler
from handlers.visual import ClusterVisualHandler,DetailsVisualHandler
def run():
	SETTING = dict(
		template_path = os.path.join(os.path.dirname(__file__),'templates'),
		static_path = os.path.join(os.path.dirname(__file__),'static')
	)
	app = tornado.web.Application(
		handlers=[
		(r'/home',MainHandler),
		(r'/show.*',ClusterVisualHandler),
		(r'/details.*',DetailsVisualHandler)
		]
		,**SETTING
	)
	print('server start...')
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen('8081')
	tornado.ioloop.IOLoop.instance().start()
	pass

if __name__=="__main__":
	run()