# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

user_ids = []

f=open('weibo_uid.txt')
for line in f.readlines():
    user_ids.append(line.strip())

for i in range(1,11):
    link = 'https://weibo.cn/pub/top?cat=star&page=' + str(i)
    r = requests.get(link,headers={'User-Agent':'Mozialla/5.0'})
    infos = re.findall('<a href="https://weibo.cn/u/.*?" class="nk">.*?</a>',r.text)
    for info in infos:
        code = re.search('/\d+"',info).group()[1:-1]
        if code not in user_ids:
            with open('weibo_uid.txt','a') as f:
                f.write(code+'\n')
                
                
url ='https://weibo.cn/5556869758/follow'
headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'accept-encoding':'gzip, deflate, br',
'accept-language':'en,zh-CN;q=0.9,zh;q=0.8',
'cache-control':'max-age=0',
'cookie':'SCF=Avlv1_MFMTz30Ps2w_AmO-Govoh2o0sYEkUrfe1ThLIv6xnMB-PibljiRAejm_POcnd756j654RZ2aoExXqlksk.; ALF=1575898623; _T_WM=493324f84d0b1550db3e0d095a2d9165; SUB=_2A25wz9CyDeRhGeNG7VcW8ivOyTiIHXVQM_D6rDV6PUJbkdAKLVHVkW1NSydJQDKmlDb-6jN3B4uY_bFE7p-Se8-A; SUHB=0gHyJtnbqK8Z2v',
'referer':'https://weibo.cn/u/2006455031',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
r = requests.get(url,headers=headers)
soup = BeautifulSoup(r.text,'lxml')
tables = soup.find_all('table')
for table in tables:
    link = table.find('a')['href']
    follow_id = link.split('/')[-1]
    if follow_id.isdigit() and follow_id not in user_ids:
        with open('weibo_uid.txt','a') as f:
                f.write(follow_id+'\n')
                