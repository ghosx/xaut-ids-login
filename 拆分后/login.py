import re
import requests
class login(object):
	"""docstring for login"""	
	def __init__(self, User,Passwd):
		super(login, self).__init__()
		self.User = User
		self.Passwd =Passwd
	def login(self):
		s = requests.session()
		headers = {
		'Host': 'my.xaut.edu.cn',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/index.portal',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1'
		}
		url = 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal'
		html = s.get(url).text
		lt = re.search(r'name="lt" value="(\S+)"',html)[1]
		execution = re.search(r'name="execution" value="(\S+)"',html)[1]
		_eventId = re.search(r'name="_eventId" value="(\S+)"',html)[1]
		data = {'username':self.User,
				'password':self.Passwd,
				'lt':lt,
				'execution':execution,
				'_eventId':_eventId,}
		res = s.post('http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal',data=data,allow_redirects=False,headers=headers)
		ticket = res.headers['Location']
		if ticket:
			s.get(s.get(ticket,allow_redirects=False).headers['Location'])
			res = s.get(ticket.split()[0],allow_redirects=False,headers=headers)
			Location = res.headers['Location']
			s.get(Location.split()[0])
			return True
		else:
			return False
