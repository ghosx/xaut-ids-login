import re
import requests

def FuckUnicode(s):
	return re.sub(';','',re.sub('&#x',r'\u',s)).encode('utf-8').decode('unicode_escape')
def lib():
	headers = {
		'Host': 'my.xaut.edu.cn',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Referer':'http://my.xaut.edu.cn/index.portal',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1'
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
def finance():
	info = []
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Cache-Control':'no-cache',
		'Connection':'keep-alive',
		'Host':'202.200.112.65',
		'Pragma':'no-cache',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
	}
	url = 'http://202.200.112.65/tysfrz/'
	s.get(url+'caslogin.aspx')
	url = url+'jump.aspx?sysid=wscx'
	html = s.get(url,headers=headers).content.decode('utf-8')
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
		html = s.post('http://202.200.112.65/web50/Views/Jgcwxx/Welcome.aspx',data=data,headers=headers).content.decode('utf-8')
		b = pattern.findall(html)
		for l in b:
			info.append(l)
	try:
		# 有的学生没有银行账号信息
		xh = re.search('学号：\s+</td>\s+<td width="15%">\s+<span id="(?:[^">]+)">(\d+)',html)[1]
		yhkh = re.search('银行账号：</td>\s+<td colspan="9">\s+<span id="(?:[^">]+)">(\d+)</span>',html)[1]
		return (info,xh,yhkh)
	except:
		return (info,False,False)

