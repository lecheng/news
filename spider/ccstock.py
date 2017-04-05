# -*- coding: utf-8 -*-
import sys
import re
from pyquery import PyQuery as pq
import time
sys.path.append('..')
from util.httputil import get_url
from dao.database import save_paper

class CCStockSpider:
	def __init__(self):
		self.title = ""
		self.url = ""
		self.source = ""
		self.spider = "CCStockSpider"
		self.content = ""
		self.comment = ""
		self.scan = ""
		self.time = ""
		self.timestamp = 0
		pass

	def parser(self,content):
		pyquery = pq(content)
		lists = pyquery('.listMain li')
		for i in lists:
			dom = pq(i)
			if dom('a'):
				self.title = dom('a').text()
				self.url = dom('a').attr('href')
				self.extract_content(self.url)
				self.save()
		pass

	def extract_content(self,url):
		content = get_url(url)
		dom = pq(content)
		self.source = dom('.sub_bt span').text()[5:-25]
		self.time = dom('.sub_bt span').text()[-16:] + ":00"
		self.timestamp = int(time.mktime(time.strptime(self.time,'%Y-%m-%d %H:%M:%S')))
		self.content = dom('#newscontent').html()
		pass

	def start(self):
		page = 1
		while(1):
			if page > 15:
				break
			url = "http://www.ccstock.cn/stock/gupiaoyaowen/index_p" + str(page) +  ".html"
			content = get_url(url)
			self.parser(content)
			page += 1
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
		print(d)
		save_paper(d)

	def run(self):
		pass

if __name__ == "__main__":
	spider = CCStockSpider()
	spider.start()
	pass
