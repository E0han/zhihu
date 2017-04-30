#10minemail-api
#2017.4.29note，第46行左右，需要用re把"locate="去掉，直接保留url后缀，等知乎恢复邮箱注册，探究知乎发给10minemail的规律
import requests
from bs4 import BeautifulSoup
import json
import re
url="https://10minutemail.net"
header_data={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'referer':"https://10minutemail.net/error-due.html",
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
	}
class email():
	session=None
	def __init__(self):
		global session
		session=requests.session()
		#self.get_emailaddress()#第一个函数，直接return 邮箱地址
		#self.get_content()
		#self.vertify_email()
	def get_emailaddress(self):#获取新的邮箱地址
		global session
		global header_data
		global url
		r=session.get(url,headers=header_data,verify=True)
		r.encoding='utf-8'
		soup = BeautifulSoup(r.text, 'html.parser')
		self.save_cookies()
		return soup.input["value"]#返回邮箱地址
	def get_content(self):
		global session
		global header_data
		global url
		letterurl=url+'/readmail.html?mid=welcome'
		self.read_cookies()
		r=session.get(letterurl,headers=header_data,verify=True)
		r.encoding='utf-8'
		soup = BeautifulSoup(r.text, 'html.parser')
		for x in soup.find_all('h1'):# will give you all a tag
			print(x)#在这里会打印邮件的所有内容，使用此脚本的用户需要自己寻找知乎验证邮件地址，在终端里将其复制并粘贴至下一阶段
	def vertify_email(self):
		global session
		global header_data
		verify_emailaddress=input("请输入验证邮件地址:")
		session.get(verify_emailaddress,headers=header_data,verify=True)

	def save_cookies(self):#保存cookie
		global session,path_for
		with open('./'+"emailcookiefile",'w')as f:
			json.dump(session.cookies.get_dict(),f)
	def read_cookies(self):#使用cookie
		global session,path_for
		#_session.cookies.load()
		#_session.headers.update(header_data)
		with open('./'+'emailcookiefile')as f:
			cookie=json.load(f)
			session.cookies.update(cookie)