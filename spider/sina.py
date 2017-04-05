# -*- coding: utf-8 -*-
import sys
from pyquery import PyQuery as pq
import time
import json
sys.path.append('..')
from util.httputil import get_url
from dao.database import save_paper

class SinaSpider:
	def __init__(self):
		self.title = ""
		self.url = ""
		self.source = ""
		self.spider = "SinaSpider"
		self.content = ""
		self.comment = ""
		self.scan = ""
		self.time = ""
		self.timestamp = 0
		pass

	def parser(self,content):
		jsonstr = content[19:-2]
		jsonobj = json.loads(jsonstr)
		lists = jsonobj['data']
		for list in lists:
			self.title = list.get('title')
			self.url = list.get('url')
			self.source = list.get('media')
			self.time = list.get('create_date') + ' ' + list.get('create_time')
			self.timestamp = int(time.mktime(time.strptime(self.time,'%Y-%m-%d %H:%M:%S')))
			self.extract_content(self.url)
			self.save()
		pass

	def extract_content(self,url):
		content = get_url(url,code='gb2312')
		dom = pq(content)
		p = dom('#artibody p')
		content = ""
		for i in p:
			dom = pq(i)
			content += dom.text() + '\n'
		self.content = content
		pass

	def start(self):
		pass
	def save(self):
		d = {
			'title': self.title,
			'url': self.url,
			'source': self.source,
			'spider': self.spider,
			'content': self.content,
			'comment': self.comment,
			'scan': self.scan,
			'time': self.time,
			'timestamp': self.timestamp
		}
		save_paper(d)
	def run(self):
		current_date = time.strftime('%Y%m%d',time.localtime(time.time()))
		url = "http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_not_url=/ustock/&top_type=day&top_cat=stock&top_time="\
			 + str(current_date) + "&top_show_num=100&top_order=ASC&js_var=stock_1_data"
		content = get_url(url)
		self.parser(content)
		pass

if __name__ == "__main__":
	spider = SinaSpider()
	spider.run()
	pass
