import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.weather.com.cn/weather/101280101.shtml')
content = res.text.encode('iso-8859-1')
soup = BeautifulSoup(content, 'html.parser')

list_day = []
i = 0
day_list = soup.find_all('h1')
for each in day_list:
    if i <= 6:
        list_day.append(each.text.strip())
        i += 1

tem_list = soup.find_all('p', class_='tem')
i = 0
list_tem = []
for each in tem_list:
    list_tem.append([each.span.text, each.i.text])
    i += 1

list_wind = []
wind_list = soup.find_all('p', class_='win')
for each in wind_list:
    list_wind.append(each.i.text.strip())
for n in range(3):
    print(list_day[n], list_tem[n], list_wind[n])
