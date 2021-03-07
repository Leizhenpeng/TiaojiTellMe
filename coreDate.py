import csv
import requests
import bs4
import chardet
import yagmail
from urllib.parse import urlparse
import sqlite3
import os
from configparser import ConfigParser



# 由于本程序需要封装,函数尽可能写在一个文件
# 定义文件读取函数
def readCsv(path,index=None):
	pool = []
	csv_reader = csv.reader(open(path,errors = "ignore",encoding = "utf-8-sig",),delimiter = ',')
	if index == None:
		for row in csv_reader:
			pool.append(row)
		return pool
	else:
		for row in csv_reader:
			pool.append(row[index])
		return pool


# 标注是否命中
def tagTiaoji(keyword,link):
	# print(link)
	# headers["Host"] = urlparse(link).netloc
	title = None
	try:
		response = requests.get(url = link,headers = headers)
		TextOut = response.content
		Char = chardet.detect(TextOut)["encoding"]
		if keyword in TextOut.decode(Char):
			# print("命中")
			try:
				soup = bs4.BeautifulSoup(TextOut,"html.parser")
				for each in soup.findAll("a"):
					atext = each.text
					if keyword in atext:
						title = each.text
						# print(title)
						break
			except Exception as e:
				pass
				print(e)
			return [True,title]
		else:
			return [False,title]
	except:
		return [False,title]




def insertValue(school,title):
	'''
	插入字段
	:param school:
	:type school:
	:param title:
	:type title:
	:return:
	:rtype:
	'''
	# school="zuel"
	# title ="其实我了"
	sql = ''' insert into schoolInfo
	             (school, title)
	             values
	             (:st_school, :st_title)'''
	cursor.execute(sql,{'st_school': school,'st_title': title})
	conn.commit()


def judgeExist(school,title):
	# school="Hust"
	# title ="其实我了"
	#

	sql = f'''select * from schoolInfo where school == "{school}" and  title=="{title}" '''
	results = cursor.execute(sql)
	all_students = results.fetchall()
	if len(all_students) == 0:
		return False
	else:
		return True


# sqlite数据库去重

# 读取学校资料
schoolList = readCsv("./target.csv")

config = ConfigParser()
config.read('user.config', encoding='UTF-8')


user = config['fromMail']['USERMAIL']
password = config['fromMail']["SMTPPASSWORD"]
host =config['fromMail']["HOST"]

target = [config["toMail"]["TOMAILADDRESS"]]
fromName = "TELL ME NOW"
keyword = config["keyword"]["SEARCH"]




headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',}

yag = yagmail.SMTP(user = user,password = password,host = host)
# 创建/连接缓存数据库
# 判断数据库是否存在
if not os.path.isfile("./info.db"):
	# 不存在就新建表格
	conn = sqlite3.connect("./info.db")
	cursor = conn.cursor()
	sql = '''create table schoolInfo (
	        school text,
	        title text,
	        time TimeStamp NOT NULL DEFAULT (datetime('now','localtime')))
	        '''
	cursor.execute(sql)
else:
	conn = sqlite3.connect("./info.db")
	cursor = conn.cursor()


for each in schoolList:
	url = each[-1]
	subject = each[0]
	school = each[1]
	tag,title = tagTiaoji(f"{keyword}",url)
	# 如果命中..
	if tag:
		ExistTag = judgeExist(school,title)
		# 如果之前不存在函数
		if not ExistTag:
			print(school,f"-----找到新的{keyword}信息-----!")
			insertValue(school,title)
			target = target
			cc = None
			if title:
				objects = f"{subject}---{school},有{keyword}相关内容:{title},传送门如下"
			else:
				objects = f"{subject}---{school},有{keyword}相关内容,传送门如下"
			contents = [url]
			fromname = {'From': fromName}
			# 发送邮件
			yag.send(to = target,subject = objects,contents = contents,cc = cc,headers = fromname)
		else:
			print(school,f"-----暂无*新的*{keyword}信息-----!")
	else:
		print(school,f"-----暂无{keyword}信息-----!")
cursor.close()
