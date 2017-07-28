import requests
from bs4 import BeautifulSoup
import re

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
def login(ticket):
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
		return data
def lib():
	dict = {}
	headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
			'Connection':'keep-alive',
			'Cookie':'PHPSESSID=ST-139825-cOO1F2SpNs1U2fTds2YN-NT3d-cas-1501222114688',
			'DNT':'1',
			'Host':'202.200.117.7:8080',
			'Referer':'http://202.200.117.7:8080/reader/redr_info.php',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
		}
	proxies = {'http' : "socks5://127.0.0.1:1080"}
	a = s.get('http://202.200.117.7:8080/reader/redr_info.php',proxies=proxies,headers=headers)
	soup = BeautifulSoup(a.content,'html.parser')
	table = soup.find('table',attrs={'style':'padding:5px'})
	for tr in table:
		for td in tr:
			m = re.search(r'^<td\s*\S*><span\s+class="bluetext">(\S+)：</span>\s?(\S*)\s?</td>$',str(td))
			if m != None:
				dict.update({m.group(1):m.group(2)})
	return dict
def lend_history():
	List = []
	headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
			'Connection':'keep-alive',
			'Cookie':'PHPSESSID=ST-139825-cOO1F2SpNs1U2fTds2YN-NT3d-cas-1501222114688',
			'DNT':'1',
			'Host':'202.200.117.7:8080',
			'Referer':'http://202.200.117.7:8080/reader/book_hist.php',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
		}
	proxies = {'http' : "socks5://127.0.0.1:1080"}
	his = s.get('http://202.200.117.7:8080/reader/book_hist.php',proxies=proxies,headers=headers)
	soup = BeautifulSoup(his.content,'html.parser')
	table = soup.find('table',attrs={'bgcolor':'#CCCCCC'})
	for tr in table:
		for td in tr:
			n = re.search(r'<td[\s\S]*>(\S+)</td>',str(td))
			if n != None:
				List.append(n.group(1))
	print(List[6::])

User = ''
Passwd = ''
ticket = ticket(User,Passwd)
login(ticket)
lend_history()