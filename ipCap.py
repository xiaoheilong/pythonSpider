import requests
from bs4 import BeautifulSoup
url = "http://www.yunarm.com/admin"
page = requests.get(url)
#print(page.status_code)
print(page.content)
soup = BeautifulSoup(page.content, 'html.parser')
str = soup.find('layui-layout layui-layout-admin')
print(str)
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