#-*- coding: utf-8 -*-
import re
import csv
import requests
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import RequestException

def get_one_page(city, keyword, page):
	#获取网页html内容并返回
	paras = {
		'jl':city,
		'kw':keyword,
		'sm':0,
		'isfilter':1,
		'p':page,
	}
	#请求头
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
		'Host': 'sou.zhaopin.com',
		'Referer':'https://www.zhaopin.com/',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'+urlencode(paras)
	try:
		#获取网页内容，返回html数据
		response = requests.get(url, headers=headers)
		#判断是否获取成功
		if response.status_code == 200:
			return response.text
		return None
	except RequestException as e:
		return None
def parse_one_page(html):
	#解析代码，提取有用信息
	#正则
	pattern = re.compile('<a style=.*? target="_blank">(.*?)</a>.*?'
		'<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a>.*?'
		'<td class="zwyx">(.*?)</td>',re.S)
	#匹配符合内容的条件
	items = re.findall(pattern,html)

	for item in items:
		job_name = item[0]
		job_name = job_name.replace('<b>','')
		job_name = job_name.replace('</b>','')
		yield {
			'job': job_name,
			'website': item[1],
			'company': item[2],
			'salary': item[3]
		}

def write_csv_headers(path, headers):
	#写入表头
	with open(path, 'a', encoding='gb18030', newline='') as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writeheader()

def write_csv_rows(path, headers, rows):
	#写入行
	with open(path, 'a', encoding='gb18030', newline='') as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writerows(rows)

def main(city, keyword, pages):
	#主函数
	filename = 'zl'+city+'-'+keyword+'.csv'
	headers = ['job', 'website', 'company', 'salary']
	write_csv_headers(filename, headers)
	for i in tqdm(range(pages)):
		#获取页面所有信息，写入csv文件
		jobs = []
		html = get_one_page(city, keyword, i)
		items = parse_one_page(html)
		for item in items:
			jobs.append(item)
		write_csv_rows(filename, headers,jobs)

if __name__== '__main__':
	main('上海', 'python工程师', 10)
# #构造请求地址
# paras = {
# 	'jl':'上海',
# 	'kw':'python工程师',
# 	'sm':0,
# 	'isfilter':1,
# 	'p':1,
# }
# url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'+urlencode(paras)