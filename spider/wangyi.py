# -*- coding: utf-8 -*-
import sys
from pyquery import PyQuery as pq
import time
sys.path.append('..')
from util.httputil import get_url
from dao.database import save_paper

class WangYiSpider:
	def __init__(self):
		self.title = ""
		self.url = ""
		self.source = ""
		self.spider = "WangYiSpider"
		self.content = ""
		self.comment = ""
		self.scan = ""
		self.time = ""
		self.timestamp = 0
		pass

	def parser(self,content):
		pyquery = pq(content)
		lists = pyquery('.article')
		for i in lists:
			dom = pq(i)
			self.title = dom('a').text()
			self.url = dom('a').attr('href')
			self.extract_content(self.url)
			self.save()
		pass

	def extract_content(self,url):
		content = get_url(url,code='gb2312')
		dom = pq(content)
		self.source = dom('#ne_article_source').text()
		self.comment = dom('.ep-tie-top a:last').text()
		self.time = dom('.ep-time-soure.cDGray').text()[:19]
		self.timestamp = int(time.mktime(time.strptime(self.time,'%Y-%m-%d %H:%M:%S')))
		self.content = dom('#endText').html()
		pass

	def start(self):
		first_url = "http://money.163.com/special/00251LR5/gundongyaowen.html"
		content = get_url(first_url,code='gb2312')
		self.parser(content)
		page = 2
		while(1):
			if page > 9:
				break
			url = "http://money.163.com/special/00251LR5/gundongyaowen_0" + str(page) + ".html"
			content = get_url(url,code='gb2312')
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
		save_paper(d)
	def run(self):
		first_url = "http://money.163.com/special/00251LR5/gundongyaowen.html"
		content = get_url(first_url,code='gb2312')
		self.parser(content)
		pass

if __name__ == "__main__":
	spider = WangYiSpider()
	spider.run()
	pass
