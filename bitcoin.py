# -*- coding:utf-8 -*-
import urllib.error
import urllib.request
import re
import requests
import random
import hashlib
from pprint import pprint
from altcoin import altcoin

#appid = '20170410000044507'
#secretKey = 'LgyBWqvu3uxwyo8BFg8v'
appid = '20151113000005349'
secretKey = 'osubCEzlGjzvw8qdQc41'

patternData = re.compile(u'<td style.*?">(.*?)</td>.*?<td.class="middletext".*?>.*?on.(.*?)</td>.*?<div.class="post">(.*?)</td>',re.S)
patternCount = re.compile(u'<td><b>Name: </b></td>.*?<td>(.*?)</td>.*?<td><b>Posts: </b></td>.*?<td>(.*?)</td>.*?<td><b>Last Active: </b></td>.*?<td>(.*?)</td>',re.S)

class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    #removeAddr = re.compile('<a.*?>|</a>')
    removeAddr = re.compile('<a.*?</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #'符号
    replaceDanYinHao = re.compile('&#039;')
    #"符号
    replaceShuangYinHao = re.compile('&quot;')
    #空格符号
    replaceSpace = re.compile('&nbsp;')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"",x)
        x = re.sub(self.replaceTD,"",x)
        x = re.sub(self.replacePara,"",x)
        x = re.sub(self.replaceBR,"",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.replaceDanYinHao,"\'",x)
        x = re.sub(self.replaceShuangYinHao,"\"",x)
        x = re.sub(self.replaceSpace," ",x)
        x = re.sub('&gt;',">",x)
        x = re.sub('&amp;',"&",x)
        x = re.sub('&lt;',"<",x)
        x = re.sub('\n',"",x)
        x = re.sub('\t',"",x)
        #strip()将前后多余内容删除
        return x.strip()
    
def GeTranslate(q):
    myurl ='http://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey

    m1 = hashlib.md5(sign.encode(encoding='gb2312'))
    sign = m1.hexdigest()
    #myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        r = requests.get(myurl,verify = False)
        if 'trans_result' in r.json().keys():
            print('=====gggggggggggggg')
            return str(r.json()['trans_result'][0]['dst'])
        elif 'error_code' in r.json().keys():
            print('=====yyyyyyyyyyyyyyyyy')
            return str(r.json()['error_code'])
        else:
            return str("nothing")
    except Exception as e:
        if hasattr(e,"code"):
            print (e.code)
        if hasattr(e,"reason"):
            print (e.reason)
        return str(e)
        
def GetPostData():
    uid = 159191
    url = 'https://bitcointalk.org/index.php?action=profile;u='+ str(uid) +';sa=showPosts'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        request = urllib.request.Request(url,headers = headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        #patternData = re.compile(u'<td style.*?">(.*?)</td>.*?<td.class="middletext".*?>.*?on.(.*?)</td>.*?<div.class="post">(.*?)</td>',re.S)
        items = re.findall(patternData,content)
        items = items[0:7]
        #序号 时间 英文原文 中文翻译
        for item in items:
            haveImg = re.search("img",item[2])
            #if not haveImg:
            zhw = GeTranslate(tool.replace(item[2]))
            #zhw = 'ggg'
            print(item[0].strip()+'\n'+tool.replace(item[1])+'\n'+tool.replace(item[2])+'\n'+zhw)
    except urllib.request.URLError as e:
        if hasattr(e,"code"):
            print (e.code)
        if hasattr(e,"reason"):
            print (e.reason)

#获取uid的昵称 post 最后上线时间
def GetPostCount():
    uid = 159191 
    url = 'https://bitcointalk.org/index.php?action=profile;u=' + str(uid)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        request = urllib.request.Request(url,headers = headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        #patternCount = re.compile(u'<td><b>Name: </b></td>.*?<td>(.*?)</td>.*?<td><b>Posts: </b></td>.*?<td>(.*?)</td>.*?<td><b>Last Active: </b></td>.*?<td>(.*?)</td>',re.S)
        items = re.findall(patternCount,content)
        for item in items:
            print(item[0].strip()+'\n'+item[1].strip()+'\n'+tool.replace(item[2]))
    except urllib.request.URLError as e:
        if hasattr(e,"code"):
            print (e.code)
        if hasattr(e,"reason"):
            print (e.reason)
            

tool = Tool()            
#GetPostCount()
GetPostData()
for alt in altcoin:
   #print(type(alt))
   print('name:',alt.get('name'))
   print('uid:',alt.get('uid'))
   print('post:',alt.get('post'))
   alt['post']=2333
   print('post:',alt.get('post'))
with open('/altcoin1.txt', 'w') as f:
    #f.write(str(altcoin))
    f.write('111')
