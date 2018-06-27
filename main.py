import requests
from pymongo import MongoClient
import os
import sys
import fileinput
import initialization
import re

# Создадим каталоги: 
initialization.makeFolders()
# Подключимся к БД:
client = MongoClient('localhost', 27017)
db = client.CatsAndDogs
collection = db.CatsAndDogs_items

# Скачаем файл с wnid:
initialization.getWNIDCollection()
# Поищем wnid, в которых есть cat[s]

file = open('wnid.txt', 'r', encoding='utf-8')
raw = file.readlines()
pattern = r'[ \t]cat[\n s]'
myCats = ''

for i in raw:
    if re.search(pattern, i) != None:
        myCats+=i
file.close()
# Запишем найденные строки в файл, чтобы всегда были под рукой
file = open('myCats.txt', 'w', encoding='utf-8')
file.write(myCats)
file.close()
# Проделав те же процедуры, отыщем dog[s]

file = open('wnid.txt', 'r', encoding='utf-8')
raw = file.readlines()
pattern = r'[ \t]dog[\n s]'
myDogs = ''

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

pattern = r'n[0-9]{8}'
# Пусть сначала будут кошечки ^_^

fileName = 'myCatsLinks.txt'
links = ''
file_read = open('myCats.txt', 'r', encoding='utf-8')
raw = file_read.readlines()

for i in raw:
    print(i)
    link = re.search(pattern, i).group()
    links+=initialization.getWNID(link)
file = open(fileName, 'w', encoding = 'utf-8')
file.write(links)
file.close()
file_read.close()

# Теперь можно и собакенов:

fileName = 'myDogsLinks.txt'
links = ''
file_read = open('myDogs.txt', 'r', encoding='utf-8')
raw = file_read.readlines()

for i in raw:
    print(i)
    link = re.search(pattern, i).group()
    links+=initialization.getWNID(link)
file = open(fileName, 'w', encoding = 'utf-8')
file.write(links)
file.close()
file_read.close()

# Теперь у нас есть все, чтобы наконец-то заполучить в свои лапы картинки (а в тех, 
# где Cats иногда такое встречается, что лучше смотреть в одиночестве, да...)

# Для url-ов используем опять же регулярку(ибо не всё, что мы получили - урлы. Боже, храни гугл...

pattern = r'(http|https)\://([a-zA-Z0-9\-\.]+\.+[a-zA-Z]{2,3})(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~]*)[^\.\,\)\(\s]?'
pattern_type = r'[.][a-zA-Z]{3}\n'

count = 100 # Возьмем, для начала 100 картинок
i = 0
file = open('myCatsLinks.txt', 'r', encoding = 'utf-8')
raw = file.readlines()
j = 0 # Тут будем считать количество уже полученных картинок
path = 'data/train/cat/'
# В цикле сделаем простейший конечный автомат, который отделит tran-файлы от test-файлов. 
# Для этого введем переменную состояния status:
status = True
for i in raw:
    if status:
        print(i)
        if re.search(pattern, i) != None and re.search(pattern_type, i) != None:
            url = re.search(pattern, i).group()
            type_file = re.search(pattern_type, i).group()
            type_file = re.sub(r'^\s+|\n|\r|\s+$','', type_file)
        else: continue
        if initialization.getImages(url, path+'cat'+str(j)+type_file):
            j+=1
            collection.insert_one({"category":"кошка", "path":path+'cat'+str(j)+type_file})
        if j >= count*0.8:
            status = False
            path = 'data/test/cat/'
            j = 0
    elif j < count*0.2:
        if re.search(pattern, i) != None and re.search(pattern_type, i) != None:
            url = re.search(pattern, i).group()
            type_file = re.search(pattern_type, i).group()
            type_file = re.sub(r'^\s+|\n|\r|\s+$','', type_file)
        else: continue
        if initialization.getImages(url, path+'cat'+str(j)+type_file):
            j+=1
            collection.insert_one({"category":"кошка", "path":path+'cat'+str(j)+type_file})
    else: break
file.close()
# Перейдем к собакенам:
i = 0
file = open('myDogsLinks.txt', 'r', encoding = 'utf-8')
raw = file.readlines()
j = 0

path = 'data/train/dog/'

status = True
for i in raw:
    if status:
        print(i)
        if re.search(pattern, i) != None and re.search(pattern_type, i) != None:
            url = re.search(pattern, i).group()
            type_file = re.search(pattern_type, i).group()
            type_file = re.sub(r'^\s+|\n|\r|\s+$','', type_file)
        else: continue
        if initialization.getImages(url, path+'dog'+str(j)+type_file):
            j+=1
            collection.insert_one({"category":"собака", "path":path+'dog'+str(j)+type_file})
        if j >= count*0.8:
            status = False
            path = 'data/test/dog/'
            j = 0
    elif j < count*0.2:
        if re.search(pattern, i) != None and re.search(pattern_type, i) != None:
            url = re.search(pattern, i).group()
            type_file = re.search(pattern_type, i).group()
            type_file = re.sub(r'^\s+|\n|\r|\s+$','', type_file)
        else: continue
        if initialization.getImages(url, path+'dog'+str(j)+type_file):
            j+=1
            collection.insert_one({"category":"собака", "path":path+'dog'+str(j)+type_file})
    else: break
file.close()