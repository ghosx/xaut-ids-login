import pymysql

# 修改数据库配置信息
config={"host":"localhost", 
			"port":3306,
			"user":"mysql",
			"passwd":"",
			"db":"test",
			"charset":'utf8'}

def lib_insert(i,h,**config):
	# i是lib()返回的read_info,h是lib()返回的read_his
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
def finance_insert(*i):
	# 这个数据库不会建
	pass