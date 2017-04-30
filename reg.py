#zhihu_register by 0han
#version=1.0
#date="2017.4.29"
#coding="utf-8"

import requests,re,json,time,os,os.path,sys
from PIL import Image
import traceback
import json
import emailget
import account_info
import proxy
import random
print("知乎账号注册系统 by 0han v1.0\n正在获取最新代理ip，请耐心等待")
_zhihu_url='https://www.zhihu.com'
_captcha_url=_zhihu_url+'/captcha.gif?r='
_captcha_url_end="&type=register";
header_data={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0'
    ,'Host':'www.zhihu.com'
    ,'Upgrade-Insecure-Requests':'1'
    ,'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
    }
use_proxy=proxy.get_proxy(1)#获取代理ip及端口，这个函数会返回一个数组，包含1*10个代理，需要耐心等待
proxy_dic={}
for i in range(1):
	proxy_dic["http"]='http://'+use_proxy[0][i]+':'+use_proxy[1][i]#生成了一个代理数组，可以直接被requests调用

class Register():
	_session=None

	def __init__(self):
		self.first_step()
	def first_step(self):
		global _session
		use_proxy=proxy.get_proxy(1)#获取代理ip及端口，这个函数会返回一个数组，包含1*10个代理
		test=emailget.email()#实例化邮箱获取脚本
		new_email=test.get_emailaddress()#获取一个新的邮箱地址
		print(new_email)#展示给你看，并且自动写入“注册邮箱”
		_session=requests.session()#准备建立注册会话
		self.register_new()#注册脚本开始运行，今天是4.30，知乎仍未开放邮箱注册，所以test到这一步就停了
		test.get_content()#登录一次性邮箱，获取知乎的邮件内容，目前是test，获取的邮件是欢迎邮件，等知乎开放注册后进行修改
		test.vertify_email()#自行寻找验证邮件中网址的内容，粘贴到提示处，将会完成验证
		account_info.savedata(new_email,password)#将新的机器人账户邮箱和密码保存到目录下的txt文本中，password参数目前不存在，需要使用re将邮箱str分割
	def register_new(self):
		global _session
		global header_data
		global xsrf
		r=_session.get('https://www.zhihu.com',headers=header_data,verify=True,proxies=proxy_dic)
		self.xsrf=re.findall('name="_xsrf" value="([\S\s]*?)"',r.text)[0]
		self.input_data()
		_register_type='/register/email'
		register_data={' _xsrf':self.xsrf,'fullname':self.username,'password':self.password,'email':self.email,'captcha':self.captcha,'captcha_source':'register'}
		r=_session.post(_zhihu_url+_register_type,data=register_data,headers=header_data,verify=True,proxies=proxy_dic)
		j=r.json()
		print(j)
		c=int(j['r'])
		if c==0:
			print('register in successful')
			os.remove("code.gif")
		else:
			print('注册出现问题。。。。')
			os.remove("code.gif")
	def get_captcha(self):
		return _captcha_url+str(int(time.time()*1000))+_captcha_url_end
	def show_or_save_captcha(self,url):
		global _session
		r=_session.get(url,headers=header_data,verify=True,proxies=proxy_dic)
		with open("code.gif",'wb') as f:
			f.write(r.content)
		#显示验证码
		try:
			print("请输入验证码")
			im = Image.open("code.gif")
			im.show()
		except:
			print("请打开下载的验证码文件code.gif")
	def input_data(self):
		global email
		global password
		global question_url
		self.username=input('请输入用户名:')
		self.email=input('请输入注册邮箱:')
		self.password=input('请输入密码:')
		self.show_or_save_captcha(self.get_captcha())
		self.captcha=input('请输入验证码:')

		if re.search(r'^1\d{10}$', self.email):
			_type='phone_num'
			_register_type='/register/phone_num'
		elif re.search(r'(.+)@(.+)', self.email):
			_register_type='/register/email'
			_type='email'
		else:
			print('用户名格式不正确')
			sys.exit(1)
cl=Register()

