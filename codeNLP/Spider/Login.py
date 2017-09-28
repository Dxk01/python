# encoding: utf-8
"""
作者：liguoyu
"""
import time
from http import cookiejar

import requests
from bs4 import BeautifulSoup
import json

class Login(object):
	""" 登陆 知乎 类 实现爬取数据时的知乎账号登陆 """
	def __init__(self,Email='liguoyu_a@163.com',password='liguoyu123'):
		"""
		初始化 函数，
		初始化登陆时的headers，session，data以及
		cookies等https请求时的交互参数
		"""
		self.headers = {
			"Host": "www.zhihu.com",
			"Referer": "https://www.zhihu.com/",
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
		}
		# 使用登录cookie信息
		self.session = requests.session()
		self.session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
		try:
			# print(self.session.cookies)
			self.session.cookies.load(ignore_discard=True)
		except:
			print("还没有cookie信息")
		self.data = {
			'email': Email,
			'password': password,
			'_xsrf': self.get_xsrf(),
			"captcha": self.get_captcha(),
			'remember_me': 'true'
		}

	def get_xsrf(self):
		response = self.session.get("https://www.zhihu.com", headers=self.headers, verify=False)
		soup = BeautifulSoup(response.content, "html.parser")
		xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
		return xsrf

	def get_captcha(self):
		"""
		把验证码图片保存到当前目录，手动识别验证码
		:return:
		"""
		t = str(int(time.time() * 1000))
		captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
		# print(captcha_url)
		r = self.session.get(captcha_url, headers=self.headers)
		with open('captcha.jpg', 'wb') as f:
			f.write(r.content)
		captcha = raw_input("验证码：")
		return captcha

	def login(self):
		login_url = 'https://www.zhihu.com/login/email'
		# print(self.session.cookies)
		response = self.session.post(login_url, data=self.data, headers=self.headers)
		login_code = response.json()
		print(login_code['msg'])

	def getSession(self):
		return self.session

	def setSession(self,session):
		self.session = session

	def getHeaders(self):
		return self.headers

	def getData(self):
		return self.data

	def setSessionCookies(self,cookies):
		self.session.cookies = cookies

def main():
	login = Login()
	login.login()

if __name__ == '__main__':
	main()




