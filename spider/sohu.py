# -*- coding: utf-8 -*-
import sys
import re
from pyquery import PyQuery as pq
import time
sys.path.append('..')
from util.httputil import get_url
from dao.database import save_paper

class SohuSpider:
	def __init__(self):
		self.title = ""
		self.url = ""
		self.source = ""
		self.spider = "SohuSpider"
		self.content = ""
		self.comment = ""
		self.scan = ""
		self.time = ""
		self.timestamp = 0
		pass

	def parser(self,content):
		pyquery = pq(content)
		lists = pyquery('.f14list li')
		for i in lists:
			dom = pq(i)
			if dom('a'):
				self.title = dom('a').text()
				self.url = dom('a').attr('href')
				self.extract_content(self.url)
				self.save()
		pass

	def extract_content(self,url):
		content = get_url(url,code='gb2312')
		dom = pq(content)
		self.source = dom('#media_span').text()
		self.time = dom('#pubtime_baidu').text()
		self.timestamp = int(time.mktime(time.strptime(self.time,'%Y-%m-%d %H:%M:%S')))
		self.comment = dom('#changyan_parti_unit').text()
		self.content = dom('#contentText :eq(0)').html()
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
		first_url = "http://stock.sohu.com/news/index.shtml"
		content = get_url(first_url,code='gbk')
		dom = pq(content)
		script = dom('.pages table td script').text()
		max_page = re.findall(r'\d+',script)[0]
		self.parser(content)
		page = int(max_page)-1
		while(1):
			if page < int(max_page)-20:
				break
			url = "http://stock.sohu.com/news/index_" + str(page) +  ".shtml"
			content = get_url(url,code='gbk')
			self.parser(content)
			page -= 1
		pass

if __name__ == "__main__":
	spider = SohuSpider()
	spider.run()
	pass
