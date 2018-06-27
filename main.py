import requests
from pymongo import MongoClient
import os
import sys
import fileinput
import initialization
import re

client = MongoClient('localhost', 27017)
db = client.test
collection = db.users
print(collection.find_one())


# initialization.getWNID('n02084071')
# initialization.deleteNullStrings('n02084071_id.txt')

# initialization.getWNID('n02121620')
# initialization.deleteNullStrings('n02121620_id.txt')

# Поищем wnid, в которых есть cat[s]

file = open('wnid.txt', 'r', encoding='utf-8')
raw = file.readlines()
pattern = r'[ \t]cat[\n s]'
myCats = ''
#print(re.search(pattern, raw[0]))
for i in raw:
    if re.search(pattern, i) != None:
        myCats+=i
file.close()
# Запишем найденные строки в файл
file = open('myCats.txt', 'w', encoding='utf-8')
file.write(myCats)
file.close()
# Проделав ту же процедуры, отыщем dog[s]

file = open('wnid.txt', 'r', encoding='utf-8')
raw = file.readlines()
pattern = r'[ \t]dog[\n s]'
myDogs = ''
#print(re.search(pattern, raw[0]))
for i in raw:
    if re.search(pattern, i) != None:
        myDogs+=i
file.close()
# Запишем найденные строки в файл
file = open('myDogs.txt', 'w', encoding='utf-8')
file.write(myDogs)

# Теперь у нас есть файлы с нужными wnid и мы можем начать извлечение ссылок на картинки 
# (хотя стоит отметить, что такая фильтрация вряд ли даст 100% качества выборки...но машинное обучение, 
# нейросети и прочее -- разве не для таких случаев? (: )



# url = 'http://farm1.static.flickr.com/228/499699798_d5cbf79377.jpg'
# r = requests.get(url)
# print(r.status_code)
# print(r.url)
# if(url == r.url):
#     out = open('img.jpg', 'wb')
#     out.write(r.content)