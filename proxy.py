#Get_Proxy_list by 0han
#date="2017.4.29"
#coding:utf-8 python 3.5 
import requests
import bs4
import time
import pickle

#proxy_list=[]
def get_proxy(n):
	disp={}
	user_agent="User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
	head={}
	head['User_Agent']=user_agent
	proxy={}
	for i in range(n):
		url='http://www.kuaidaili.com/proxylist/'
		firsturl=url+str(i+1)+'/'
		for j in range(5):
			req=requests.get(firsturl,headers=head)
			soup = bs4.BeautifulSoup(req.text,'html.parser')
			proxy[soup.select('tbody > tr:nth-of-type('+str(j+1)+') > td:nth-of-type(1)')[0].get_text()]=soup.select('tbody > tr:nth-of-type('+str(j+1)+') > td:nth-of-type(2)')[0].get_text()
			disp[soup.select('tbody > tr:nth-of-type('+str(j+1)+') > td:nth-of-type(1)')[0].get_text()]=soup.select('tbody > tr:nth-of-type('+str(j+1)+') > td:nth-of-type(2)')[0].get_text()
			print("[*]已成功获取代理ip +1")
			time.sleep(1)
	ip=[]#为了方便调用，将字典转换为数组，将ip地址和端口放到分别的数组中，别的程式里直接按index使用
	port=[]
	total=[]
	for item in disp.keys():
			ip.append(item)
	for item in disp.values():
			port.append(item)
	total.append(ip)
	total.append(port)
	return total
#proxy_list=get_proxy(1)#这个参数是页数，每页有10条数据，n页就是10n个数据，列表可以在主函数中创建


