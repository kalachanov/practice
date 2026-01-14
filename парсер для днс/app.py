import requests
from bs4 import BeautifulSoup

header = {'user-agent': '1hfhfhfhf7373'}

url = 'https://www.dns-shop.ru'
get = requests.get(url, headers=header).text
soup = BeautifulSoup(get, 'lxml')
# block = soup.find('div', id='product-card-characteristics')
print(get)

# ! Подпроект - парсер днс для добавочной информации в сам сайт и 
# ! набиванием его базой данных.