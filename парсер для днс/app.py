import requests
from bs4 import BeautifulSoup

url = 'https://browser-info.ru/'
get = requests.get(url).text
soup = BeautifulSoup(get, 'lxml')
block = soup.find('div', id='javascript_check')
print(block)