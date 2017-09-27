import pymysql
# from config import *
import re
import sys
import time
import logging
import tablib
import time

class Query_mysql():
	def __init__(self):
		self.data = []
		self.db = pymysql.connect(host=dev_host, port=dev_port, user=dev_username, \
			passwd=dev_wp, db=dev_dbname,  charset="utf8")
		self.db3 = pymysql.connect(host=dev_host, port=dev_port, user=dev_username,\
			passwd=dev_wp, db='video_account',  charset="utf8")
		self.cursor = self.db.cursor()
		self.cursor3 = self.db3.cursor()	

	def select(self):
		for tab in dev_tab:
			if tab == 'gvs_video_':
				for x in range(64):
					sql = 'select * from ' + tab + str(x) + ' where create_time >= 1501516800 '
					try:
						self.cursor.execute(sql)
						rows = self.cursor.fetchall()
						for row in rows:
							#str(row[4]) 转换成str才可以拼接
							sql3 = 'select given_name from gvs_account where account_id = ' + str(row[4])
							self.cursor3.execute(sql3)
							r = self.cursor3.fetchone()	
							#time.localtime(row[20]) row[20]时间戳
							date = time.strftime('%m-%d %H:%M', time.localtime(row[20]))
							date = (date,)
							#python没有===
							if type(r) != tuple:
							    self.data.append(row+('',)+date)
							else:
							    self.data.append(row+r+date)	
					except Exception as e:
						logging.error('%s', str(e))
		# print(self.data)
		# sys.exit(0)				
		headers = ('''self.data列表里元祖数量一致''')
		#f = open('out.txt', 'w')
		#print(self.data, file = f)
		data = tablib.Dataset(*self.data, headers=headers)
		# print(data)
		with open('xxx.xls', 'wb') as f:
			f.write(data.export('xls'))							

	def image_replace(self, url):
		# ?非贪婪模式
		strinfo = re.compile('(https|http):\/\/.+?\/')
		b = strinfo.sub('http://uat.net.cn/',url)
		return b

	def init_logger(self):
		level = logging.DEBUG
		logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=level)		

if __name__ == '__main__':
	cli = Query_mysql()
	cli.init_logger()
	cli.select()

# print (a.replace('https://cdn.com','python') )
