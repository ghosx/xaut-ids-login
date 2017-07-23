import requests
from bs4 import BeautifulSoup
import time
s = requests.Session()

def ticket(User,Passwd):
	url = 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal'
	html = s.get(url)
	soup = BeautifulSoup(html.content,'html.parser')
	lt = soup.find('input',attrs={'name':'lt'})['value']
	execution = soup.find('input',attrs={'name':'execution'})['value']
	_eventId = soup.find('input',attrs={'name':'_eventId'})['value']
	headers = {
		'Host': 'ids.xaut.edu.cn',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1'
		}
	data = {'username':User,
			'password':Passwd,
			'lt':lt,
			'execution':execution,
			'_eventId':_eventId,}
	res = s.post('http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal',data=data,allow_redirects=False,headers=headers)
	try:
		location1 = res.headers['Location']
		a = s.get(location1,allow_redirects=False)
		location2 = a.headers['Location']
		b = s.get(location2).content
		if 'ticket' in location1:
			return location1
		else:
			return False
	except:
		return False
def go(ticket):
	headers = {
	 		'Host': 'my.xaut.edu.cn',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0' ,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6,ko;q=0.4,ja;q=0.2,en;q=0.2,en-US;q=0.2'
	}
	if ticket != False:
		res = s.get(ticket.split()[0],allow_redirects=False,headers=headers)
		Location = res.headers['Location']
		data = s.get(Location.split()[0]).text
		print(data)


User = 'XXX'
Passwd = 'XXX'
ticket = ticket(User,Passwd)
go(ticket)