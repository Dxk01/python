# encoding: utf-8
# !/usr/bin/env python
"""
作者：liuzhijun
微信： lzjun567
公众号：Python之禅（id：VTtalk）
"""
import time
from http import cookiejar

import requests
from bs4 import BeautifulSoup
import json

headers = {
	"Host": "www.zhihu.com",
	"Referer": "https://www.zhihu.com/",
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
	print(session.cookies)
	session.cookies.load(ignore_discard=True)

except:
	print("还没有cookie信息")


def get_xsrf():
	response = session.get("https://www.zhihu.com", headers=headers, verify=False)
	soup = BeautifulSoup(response.content, "html.parser")
	xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
	return xsrf


def get_captcha():
	"""
	把验证码图片保存到当前目录，手动识别验证码
	:return:
	"""
	t = str(int(time.time() * 1000))
	captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
	print(captcha_url)
	r = session.get(captcha_url, headers=headers)
	with open('captcha.jpg', 'wb') as f:
		f.write(r.content)
	captcha = raw_input("验证码：")
	return captcha


def login(email, password):
	login_url = 'https://www.zhihu.com/login/email'
	data = {
		'email': email,
		'password': password,
		'_xsrf': get_xsrf(),
		"captcha": get_captcha(),
		'remember_me': 'true'}
	print(session.cookies)
	response = session.post(login_url, data=data, headers=headers)
	login_code = response.json()
	print(login_code['msg'])
	print(session.cookies)
	# data = {'child': '19556031', 'parent': '19778317'}
	# result = get_json(session,headers,data)
	res = session.post("https://www.zhihu.com/topic/19778317/organize/entire?parent=19778317", data=data,
	                   headers=headers)
	# json_dict = res.json()
	json_topic = eval(res.text.encode("utf8"))
	i = 0
	for topic in json_topic['msg']:
		if i % 2 == 0:
			print topic[0]
			print topic[1]
			print topic[2]
		else:
			for sub_topic in topic:
				print sub_topic[0]
				print sub_topic[1]

	# json_topic = res.content['msg']
	# print json_topic


# 获取一次 request 的 json 数据
def get_json(session=None, headers=None, data=None):
	url = 'https://www.zhihu.com/topic/19776749/organize/entire'
	# data = {'child': child_id, 'parent': parent_id}
	res = session.get(url, data=data, headers=headers)
	print res.text
	# json_dict = res.json()
	return res


if __name__ == '__main__':
	email = "XXXXXa@163.com"
	password = "XXXXX"
	login(email, password)
	json_str = ""
