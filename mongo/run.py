# -*- coding: utf-8 -*-
import os

def run():
	root = "/usr/local/Cellar/mongodb/3.4.2/"

	#设置mongodb的三个路径：
		#bin,命令路径
		#data,数据路径
		#log，历史记录路径
	bin = root + "bin"
	data = root + "data/db"
	log = root + "log/data.log"

	#如果路径不存在，则创建路径
	if not os.path.exists(data):
		os.mkdir(data)
	if not os.path.exists(log):
		os.mkdir(log)

	#启动数据库命令
	cmd="./mongod"				#bin目录下的数据库服务器端
	cmd=cmd+" --port 27017 "	#设置端口，默认27017
#	cmd=cmd+" --auth"			#启动密码验证
	cmd=cmd+" --dbpath="+data	#设置数据路径
	cmd=cmd+" --logpath="+log	#设置历史记录路径
	cmd=cmd+" --logappend&"		#历史记录为追加写入
	print(bin)
	try:
		os.chdir(bin)			#切换到bin目录下
		os.popen(cmd)			#执行启动数据库命令(后台挂起）
		#os.system(cmd)			#执行启动数据库命令(前端长驻）
		print("started mongodb ...")	#提示启动成功
	except:
		print("failed mongodb")		#提示启动失败

if __name__=="__main__":
	run()

