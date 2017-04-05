# -*- coding: utf-8 -*-
import sys
import jieba
import jieba.posseg as posseg
import jieba.analyse
sys.path.append("..")


def load_userdict():

	'''载入用户字典'''
	files = ["stockdict.txt","stockword.txt"]
	path = "../file/dict/"
	for filename in files:
		jieba.load_userdict(path + filename)
load_userdict()

def keywords(content):

	'''获取内容的关键词'''
	list = []
	words = posseg.cut(content)
	for word in words:
		#print(word.word + ' ' + word.flag)
		if ('n' in word.flag or 'v' in word.flag) and word.flag !='eng':
			list += [word.word]
	keywords = jieba.analyse.extract_tags("".join(list),20,True)
	return keywords

def run():
	f = open('../file/sample/sample.txt','r',encoding='utf-8')
	content = f.read()
	print(keywords(content))
	f.close()

if __name__ == "__main__":
	run()
			




