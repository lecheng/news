# -*- coding: utf-8 -*-
#!/usr/bin/python3
import urllib.request
import io
import gzip
import chardet
import sys
import socket

def get_url(url,code='utf-8',codeset='off',retries=3):

	'''获取url的html'''
	try:
		req = urllib.request.Request(url)
	except urllib.request.URLError as e:
		print(e)
		return ""
	try:
		response = urllib.request.urlopen(req,timeout=10)
	except urllib.request.URLError as e:
		return ""
	content = response.read()
	if(response.info().get('Content-Encoding') == 'gzip'):
		compressedstream = io.BytesIO(content)
		gzipper = gzip.GzipFile(fileobj=compressedstream)
		content = gzipper.read()
	if codeset == 'on':
		code = response.info().get('Content-Type')[19:]
		if code == "":
			code = chardet.detect(content)['encoding']
	content = content.decode(code,errors='replace').replace('&nbsp',' ')
	return content
