import requests
import re
import pymysql

s = requests.session()
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
def FuckUnicode(s):
	return re.sub(';','',re.sub('&#x',r'\u',s)).encode('utf-8').decode('unicode_escape')

def login(User,Passwd):
	url = 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal'
	html = s.get(url).text
	lt = re.search(r'name="lt" value="(\S+)"',html)[1]
	execution = re.search(r'name="execution" value="(\S+)"',html)[1]
	_eventId = re.search(r'name="_eventId" value="(\S+)"',html)[1]
	data = {'username':User,
			'password':Passwd,
			'lt':lt,
			'execution':execution,
			'_eventId':_eventId,}
	res = s.post('http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal',data=data,allow_redirects=False,headers=headers)
	ticket = res.headers['Location']
	s.get(s.get(ticket,allow_redirects=False).headers['Location'])
	headers['Host'] = 'my.xaut.edu.cn'
	headers['Referer'] = 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/index.portal'
	res = s.get(ticket.split()[0],allow_redirects=False,headers=headers)
	Location = res.headers['Location']
	s.get(Location.split()[0])
	return True
def lib():
	headers = {
			'Referer':'http://my.xaut.edu.cn/index.portal',
		}
	proxies = {'http' : "socks5://127.0.0.1:1080"}
	url = 'http://ids.xaut.edu.cn:80/authserver/login?service=http://202.200.117.7:8080/reader/hwthau.php'
	Location = s.get(url,proxies=proxies,headers=headers,allow_redirects=False).headers['Location']
	html = s.get(Location,proxies=proxies,headers=headers).content.decode('utf-8')
	pattern = re.compile(r'<TD.*><span class="bluetext">(\S+)：\s*</span>\s?(\S*).*</TD>')
	read_info =  pattern.findall(html)
	url = 'http://202.200.117.7:8080/reader/book_hist.php'
	data = {'para_string':'all'}
	html = s.post(url,proxies=proxies,data=data,headers=headers).content.decode('utf-8')
	reg = r'"\d%">([^<]+)[^%]+%">([^<]+)+[^..]+../opac/item.php\?marc_no=\d+">([^<]+)[^%]+%">([^<]+)[^%]+%">([^<]+)[^%]+%">([^<]+)[^%]+%">([^<]+)'
	pattern = re.compile(reg)
	read_his = []
	for l in pattern.findall(html):
		l = list(l)
		l[2],l[3] = FuckUnicode(l[2]),FuckUnicode(l[3])
		read_his.append(l)
	return (read_info,read_his)
def insert_lib(i,h,**config):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = r"INSERT INTO `lib_info` VALUES(NULL,'"+i['读者证件号']+"','"+i['姓名']+"','"+i['性别']+"','"+i['读者条码号']+"','"+i['读者类型']\
			+"','"+i['工作单位']+"','"+i['职业']+"','"+i['职称']+"','"+i['职位']+"','"+i['生效日期']+"','"+i['失效日期']\
			+"','"+i['押金']+"','"+i['手续费']+"','"+i['累计借书']+"','"+i['违章状态']+"','"+i['欠款状态']+"')"
	cur.execute(sql)
	for l in h:
		sql = "INSERT INTO `lib_his` VALUES('"+l[0]+"','"+l[1]+"','"+l[2]+"','"+l[3]+"','"+l[4]+"','"+l[5]+\
		"','"+l[6]+"')"
		try:
			cur.execute(sql)
		except:
			pass
	conn.commit()
	cur.close()
	conn.close()
def finance():
	info = []
	url = 'http://202.200.112.65/tysfrz/'
	s.get(url+'caslogin.aspx')
	url = url+'jump.aspx?sysid=wscx'
	html = s.get(url).content.decode('utf-8')
	page = re.search(r'id="[^"]+">(\d)',html)[1]
	reg = r'<tr class="[^"]+"(?: bgcolor="[^"]+")?(?: style="[^"]+")?>\s+<td>([^<]+)</td><td>([^<]+)</td><td class="numberCol">([^<]+)</td><td align="right">\s+<a id=\S+\s+[^>]+>([^<]+)?</a>\s+</td><td align="right">\s+<a id=\S+\s+[^>]+>([^<]+)?</a>\s+</td><td align="right">\s+<a id=\S+\s+[^>]+>([^<]+)?</a>\s+</td><td class="numberCol">([^<]+)?</td>'
	pattern = re.compile(reg)
	a = pattern.findall(html)
	for l in a:
		info.append(l)
	if page != '1':
		# 翻页
		data = {
			'__VIEWSTATE':re.search(r'name="__VIEWSTATE" id="__VIEWSTATE"\s+value="([^"]+)"',html)[1],
			'ctl00$ContentPlaceHolder1$TabContainer_jf$TabPanel1$PageSpliter_zwxm_sf$LBNext.x':'6',
			'ctl00$ContentPlaceHolder1$TabContainer_jf$TabPanel1$PageSpliter_zwxm_sf$LBNext.y':'9'
		}
		html = s.post('http://202.200.112.65/web50/Views/Jgcwxx/Welcome.aspx',data=data).content.decode('utf-8')
		b = pattern.findall(html)
		for l in b:
			info.append(l)
	try:
		# 有的学生没有银行账号信息
		xh = re.search('学号：\s+</td>\s+<td width="15%">\s+<span id="(?:[^">]+)">(\d+)',html)[1]
		yhkh = re.search('银行账号：</td>\s+<td colspan="9">\s+<span id="(?:[^">]+)">(\d+)</span>',html)[1]
		return (info,xh,yhkh)
	except:
		return info
def main():
	# 修改数据库配置信息
	config={"host":"localhost", 
			"port":3306,
			"user":"mysql",
			"passwd":"",
			"db":"test",
			"charset":'utf8'}

	User = 'XXXXXX'
	Passwd = 'XXXXXX'	

	login(User,Passwd)
	print(finance())
	# insert_lib(dict(lib()[0]),lib()[1],**config)
	print("大功告成!")
if __name__ == '__main__':
	main()




