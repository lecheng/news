# -*- coding: utf-8 -*-
import sys
from pyquery import PyQuery as pq
import time
sys.path.append('..')
from util.httputil import get_url
from dao.database import save_paper

class TencentSpider:
	def __init__(self):
		self.title = ""
		self.url = ""
		self.source = ""
		self.spider = "TencentSpider"
		self.content = ""
		self.comment = ""
		self.scan = ""
		self.time = ""
		self.timestamp = 0
		pass

	def parser(self,content):
		pyquery = pq(content)
		lists = pyquery('.mod.newslist li')
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
		self.source = dom('.where').text()
		if(dom('.article-time').text()!=""):
			self.time = dom('.article-time').text() + ":00"
			print (self.time)
			self.timestamp = int(time.mktime(time.strptime(self.time,'%Y-%m-%d %H:%M:%S')))
		self.comment = dom('#cmtNum').text()
		p = dom('#Cnt-Main-Article-QQ p')
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
		first_url = "http://finance.qq.com/l/stock/gdzx/" + current_date[:6] + "/list2012121283658_"\
			+ current_date[-2:] + ".htm"
		content = get_url(first_url,code='gb2312')
		dom = pq(content)
		max_page = dom('.pageNav').children().eq(-2).text()
		print(max_page)
		self.parser(content)
		page = 2
		while(1):
			if page > int(max_page):
				break
			url = "http://finance.qq.com/l/stock/gdzx/" + current_date[:6] + "/list2012121283658_"\
				+ current_date[-2:] + "_" + str(page) + ".htm"
			content = get_url(url,code='gb2312')
			self.parser(content)
			page += 1
		pass

if __name__ == "__main__":
	spider = TencentSpider()
	spider.run()
	pass
