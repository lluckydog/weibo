import requests
import re
from bs4 import BeautifulSoup
import time
import json
import threading

user_ids = []

f=open('weibo_uid.txt')
for line in f.readlines():
    user_ids.append(line.strip())

user_infos = []
user_weibos = []

def get_info(user_id):
    user_dict = {}
    time.sleep(10)
    url = 'https://weibo.cn/{}/info'.format(user_id)
    print(url)
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en,zh-CN;q=0.9,zh;q=0.8',
        'cache-control':'max-age=0',
        'cookie':'SCF=Avlv1_MFMTz30Ps2w_AmO-Govoh2o0sYEkUrfe1ThLIv6xnMB-PibljiRAejm_POcnd756j654RZ2aoExXqlksk.; ALF=1575898623; SUB=_2A25wz9CyDeRhGeNG7VcW8ivOyTiIHXVQM_D6rDV6PUJbkdAKLVHVkW1NSydJQDKmlDb-6jN3B4uY_bFE7p-Se8-A; SUHB=0gHyJtnbqK8Z2v; _T_WM=43888046750',
        'referer':'https://weibo.cn/u/2006455031',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
            }
    r = requests.get(url,headers=headers)
    tip = re.compile(r'class="tip">(.*?)></div>', re.S)
    title=re.compile(r'(.*?)</div><div',re.S)#基本信息/学历信息
    node=re.compile(r'.*?class="c"(.*?)$',re.S)
    info=re.compile(r'>(.*?)<br/',re.S)
    tips=re.findall(tip,r.text)
    nick_name=''
    gender=''
    province=''
    city = ''
    birthday=''
    intro=''

    for one in tips:
        titleone=re.findall(title,one)#信息标题
        node_tmp=re.findall(node,one)
        infos=re.findall(info,node_tmp[0])#信息
        if(titleone[0]=='基本信息'):
            for inf in infos:
                if(inf.startswith('昵称')):
                    nick_name=inf.split(':')[1]
                elif(inf.startswith('性别')):
                    gender = inf.split(':')[1]
                elif(inf.startswith('地区')):
                    area = inf.split(':')[1].split(' ')
                    if len(area)==2:
                        province = area[0]
                        city = area[1]
                    else:
                        province = area[0]
                        city = ''
                elif(inf.startswith('生日')):
                    birthday = inf.split(':')[1]
                elif(inf.startswith('简介')):
                    intro = inf.split(':')[1]
                else:
                    pass
    user_dict['user_id'] = user_id
    user_dict['nick_name'] = nick_name
    user_dict['province'] = province
    user_dict['city'] = city
    user_dict['intro'] = intro
    user_dict['birthday'] = birthday
    user_dict['gender'] = gender
    
    fans = []
    for p1 in range(1,11):
        time.sleep(10)
        fan_url = 'https://weibo.cn/{}/fans?page={}'.format(user_id,p1)
        r = requests.get(fan_url,headers=headers)
        soup = BeautifulSoup(r.text,'lxml')
        tables = soup.find_all('table')
        for table in tables:
            link = table.find('a')['href']
            fan_id = link.split('/')[-1]
            fans.append(fan_id)
            user_dict['fans'] = fans
        
    followers = []
    for p1 in range(1,11):
        time.sleep(10)
        follow_url = 'https://weibo.cn/{}/follow?page={}'.format(user_id,p1)
        r = requests.get(follow_url,headers=headers)
        soup = BeautifulSoup(r.text,'lxml')
        tables = soup.find_all('table')
        for table in tables:
            link = table.find('a')['href']
            follow_id = link.split('/')[-1]
            followers.append(follow_id)
    user_dict['followers'] = followers
        
    user_infos.append(user_dict)
        
    time.sleep(10)
        
    main_url = 'https://weibo.cn/u/'+user_id
    print(main_url)
    r = requests.get(main_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    cons = soup.find_all('div',class_='c')
    del cons[0]
    weibos = []
    for c in cons:
        time.sleep(5)
        weibo_dict = {}
        try:
            cut_text = c.find_all('span')[-1].text.split('\xa0')
            if len(cut_text) == 2:
                created_at = cut_text[0]
                tool = cut_text[1]
            else:
                created_at = cut_text[0]
                tool = ''
            if '前' in created_at:
                content = c.find('span').text
                if c.text.startswith('转发了'):
                    author_id = c.find('span',class_='cmt').find('a')['href'].split('/')[-1]
                else:
                    author_id = user_id
                wurls = re.findall('https://weibo.cn/comment/.*?"',str(c))
                if len(wurls)==2:
                    repost_weibo_url = wurls[0]
                    weibo_url = wurls[1]
                else:
                    weibo_url = wurls[0]
                    repost_weibo_url = ''
                div = c.find_all('div')
                if len(div)==2:
                    like_num = re.search(r'赞[[\d]+]',div[1].text).group()
                    repost_num = re.search(r'转发[[\d]+]',div[1].text).group()
                    comment_num = re.search(r'评论[[\d]+]',div[1].text).group()
                
                image_group = []
                if '组图共' in c.text:
                    time.sleep(10)
                    text = str(c)
                    ptext = re.search('<a href="https://weibo.cn/mblog/picAll/.*?">',text).group()
                    pic_url = re.search('".*?"',ptext).group()[1:-1]
                    headers = {
                            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                            'accept-encoding':'gzip, deflate, br',
                            'accept-language':'en,zh-CN;q=0.9,zh;q=0.8',
                            'cache-control':'max-age=0',
                            'cookie':'SCF=Avlv1_MFMTz30Ps2w_AmO-Govoh2o0sYEkUrfe1ThLIv6xnMB-PibljiRAejm_POcnd756j654RZ2aoExXqlksk.; ALF=1575898623; SUB=_2A25wz9CyDeRhGeNG7VcW8ivOyTiIHXVQM_D6rDV6PUJbkdAKLVHVkW1NSydJQDKmlDb-6jN3B4uY_bFE7p-Se8-A; SUHB=0gHyJtnbqK8Z2v; _T_WM=43888046750',
                            'sec-fetch-mode':'navigate',
                            'sec-fetch-site':'none',
                            'sec-fetch-user':'?1',
                            'upgrade-insecure-requests':'1',
                            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
                            }
                    r = requests.get(pic_url,headers=headers)
                    pic_info = re.findall('"/mblog/pic.*?"',r.text)
                    for pic in pic_info:
                        p_link = 'https://weibo.cn' + pic[1:-1]
                        image_group.append(p_link)
                else:
                    print(c.text)
                    p_link = c.find('img')['src']
                    image_group.append(p_link)
                    print(image_group)
                weibo_dict['weibo_url'] = weibo_url
                weibo_dict['user_id'] = author_id
                weibo_dict['content'] = content
                weibo_dict['image_group'] = image_group
                weibo_dict['tool'] = tool
                weibo_dict['created_at'] = created_at
                weibo_dict['repost_num'] = repost_num
                weibo_dict['comment_num'] = comment_num
                weibo_dict['like_num'] = like_num
                weibo_dict['repost_weibo_url'] = repost_weibo_url
                    
                weibos.append(weibo_dict)
        except:
            continue
        user_weibos.append(weibos)
    
for user_id in user_ids:
    time.sleep(3)
    t = threading.Thread(target=get_info,args=(user_id,))
    t.start()

user_info = json.dumps(user_infos)
with open('user_infos.json', 'w') as u_file:
    u_file.write(user_info)
    
user_weibo = json.dumps(user_weibos)
with open('user_weibos.json', 'w') as w_file:
    w_file.write(user_weibo)

    
    