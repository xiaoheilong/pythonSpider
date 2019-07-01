import requests
import json
import gzip
from io import BytesIO
import ssl
import http.cookiejar
import urllib
from bs4 import BeautifulSoup
from urllib import request

#from lxml import etree
import os
from selenium import webdriver
import time
import re
import importlib
import sys
from PIL import Image
import pytesseract

from PIL  import Image, ImageDraw

importlib.reload(sys)
#from mysqldb import ConnectMysql
#import pymysql
ssl._create_default_https_context = ssl._create_unverified_context
# 二值化  
threshold = 140  
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  
  
#由于都是数字  
#对于识别成字母的 采用该表进行修正  
rep={'O': '0',
           'I': '1',
           'L': '1',
           'Z': '7',
           'A': '4',
           '&': '4',
           'S': '8',
           'Q': '0',
           'T': '7',
           'Y': '7',
           '}': '7',
           'J': '7',
           'F': '7',
           'E': '6',
           ']': '0',
           '?': '7',
           'B': '8',
           '@': '6',
           'G': '0',
           'H': '3',
           '$': '3',
           'C': '0',
           '(': '0',
           '[': '5',
           'X': '7',
           '`': '',
           '\\': '',
           ' ': '',
           '\n': '',
           '-': '',
           '+': '',
           '*': '',
           '.': '',
           ';': ''
           }


# 二值数组
t2val = {}


def getMainHtml(url):
    #url = "http://www.yunarm.com/admin"
    raw = {
        "username": 'ysjgly7',
        "password": 'password',
        "captcha": 'ntup',
        "remember": '1',
    }
    data = json.dumps(raw)
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8',
               'Connection': 'keep-alive',
               'Cookie': 'Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1555064760,1555983875; 03d59d43a62f5a8ded3cb0608aadd4bb=825b8fc8dd9c271aaa0c1382835e8b4c; 0_2c7212d2692a557659446c4633af6e31=78e33c11c99295f68deaa9d48d60b9af; Hm_lvt_affb9cbd1fdfa7253bd71c8e51455851=1559114611,1561619040; Hm_lpvt_affb9cbd1fdfa7253bd71c8e51455851=1561619042',
               'Host': 'www.yunarm.com',
               'Origin': 'https://www.yunarm.com',
               'Referer': 'https://www.yunarm.com/api/index/login',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    login_data = urllib.request.Request(
        url,  headers=headers, data=data.encode(encoding='UTF8'))  # .
    cj = http.cookiejar.CookieJar()  # 获取Cookiejar对象（存在本机的cookie消息）
    # 自定义opener,并将opener跟CookieJar对象绑定
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    # 安装opener,此后调用urlopen()时都会使用安装过的opener对象
    urllib.request.install_opener(opener)
    # opener.open(url,login_data).read().encode(encoding='UTF8')
    page = request.urlopen(login_data).read()
    # print(page)
    buff = BytesIO(page)

    f = gzip.GzipFile(fileobj=buff)

    res = f.read().decode('utf-8')

    # print(res)
    return res


def clickElement(element):
    print("clickElement!")


def throughAllPageByElement(element):
    print(element)
'''
def recongnizePicText(picPath):
	text=pytesseract.image_to_string(Image.open(picPath))
	return text
'''
def recongnizePicText(name):        
    #打开图片  
    im = Image.open(name)  
    #转化到灰度图
    imgry = im.convert('L')
    #保存图像
    #imgry.save('g'+name)  
    #二值化，采用阈值分割法，threshold为分割点 
    #out = imgry.point(table,'1')  
    twoValue(imgry, 100)
    #out.save('b'+name)  
    #降噪声
    clearNoise(imgry , 3, 2) 
    saveImage('b'+name , imgry.size)
    #识别  
    imageStr = 'b' + name
    recognizeImag  = Image.open(imageStr)
    text = pytesseract.image_to_string(recognizeImag)  
    print('start recongnize the image is ::' + imageStr + ' the  text is :'  + text)
    text = text.strip(' ') 
    text = text.upper(); 
    for r in rep:  
        text = text.replace(r,rep[r])  
    return text 


def downloadUrlImage(img_url, savePath):
    api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
    header = {"Authorization": "Bearer " + api_token} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(img_url, verify=False, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(savePath, 'wb').write(r.content) # 将内容写入图片
        print("download urlPicture done!")
    del r

def get_snap(driver, savePath):  # 对目标网页进行截屏。这里截的是全屏
    driver.save_screenshot(savePath)
    page_snap_obj=Image.open(savePath)
    return page_snap_obj

###
###二值插值
###
def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0



def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])
    image.save(filename)

# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败

def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1






def  capTurePicByName(driver , elementName , savePath):
    img = driver.find_element_by_id(elementName)
    #time.sleep(2)
    location = img.location
    print('location: ')
    print(location)
    size = img.size
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    page_snap_obj = get_snap(driver , savePath)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    return image_obj 


def openBrower(html):
    driver = webdriver.Chrome()
    driver.get(html)
    page = 0
    ##获取用户名和密码编辑框窗口，并
    driver.find_element_by_name('username').send_keys('ysjgly7')
    driver.find_element_by_name('password').send_keys('c1QoSD')
    #tokenStr = driver.find_element_by_id('captcha').get_attribute("src")
    #print('tokenStr' + tokenStr)
    #os.remove("./verifyPic.png")
    #downloadUrlImage(tokenStr , "verifyPic.png")
    cropImage = capTurePicByName(driver , 'captcha' , "html_full.png")
    cropImage.save("html_crop.png")
    certText = recongnizePicText("html_crop.png")

    print('certText :' + certText)
    time.sleep(2000)
def main():
    url = "http://www.yunarm.com/admin"
    openBrower(url)


if __name__ == '__main__':
    main()

#brower  = webdriver.Chrome()
#soup = BeautifulSoup(page, "html.parser")
# print(soup)
# str = soup.find('div' , class="layui-layout layui-layout-admin")
#str  = soup.find_all(name='div' , attrs ={"class": "layui-form-item"})
# print(str)
'''
#tableBox = soup.find('layui-tab-item', class_='layui-tab-box')
tabCard = soup.find('layui-tab layui-tab-card')
layuiTableBox = tabCard.find('div' , class_='layui-table-box')
tableBox = layuiTableBox.find('table' , class_='layui-table')
for link in tableBox.find_all('tr'):
	name = link.find(attrs={'data-field':'ip'})
	print(name.get_text('title'))
#tableMain = table.find();

#for link in tb.find_all('b'):

#name = link.find('a')

#print(name.get_text('title'))'''
