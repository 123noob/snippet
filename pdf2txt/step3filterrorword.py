import urllib.request
# import urllib.error
# import urllib.parse
import json
import sys
import time

def filterErrorWorld(word):
		# print(word)
		# sys.exit(0)
		url = 'https://api.shanbay.com/bdc/search/?word=' + str(word)
		req = urllib.request.Request(url,headers={
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"})
		res = urllib.request.urlopen(req)
		status = json.loads(res.read().decode('utf8'))
		print(status['msg'])
		# print(bool(status_code))
		# sys.exit(0)
		return False if status['status_code'] else True



words = []
with open('result2.txt') as f:
	for w in f.readlines():
		word = w.strip()
		if filterErrorWorld(word):
			words.append(word)
		time.sleep(2)	

with open('result3.txt','w+') as w:		
	for word in list(set(words) ):
		if len(word) > 4:
			w.write(word+'\n')


			
