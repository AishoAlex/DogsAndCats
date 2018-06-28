'''
    Получим здесь нужные нам файлы: 
    с wnid и соответственные списки картинок
'''
import fileinput
import requests
import os
def getWNIDCollection():
    r = requests.get('http://image-net.org/archive/gloss.txt')
    fileName = 'wnid.txt'
    file = open(fileName, 'w', encoding = "utf-8")
    file.write(r.text)
    file.close()
def getWNID(wnid):
    url = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid='+wnid
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:  
        print(e)
        return False
    # fileName = wnid+'_id.txt'
    # file = open(fileName, 'w', encoding = "utf-8")
    # file.write(r.text)
    # file.close()
    return r.text
def deleteNullStrings(fileName):
    # Удаляем пустые строки
    file = open(fileName, 'r', encoding='utf-8')
    raw = file.readlines()
    new = ''
    for i in raw:
        if i != '\n':
            new+=i
    file.close()
    file = open(fileName, 'w', encoding = 'utf-8')
    file.write(new)
def getImages(url, path):
    mark = False
    file = open(path, 'wb')
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:  
        print(e)
        return False
    
    if(url == r.url): # Довольно топорно, но таки работает
        file.write(r.content)
        mark = True
    file.close()
    return mark
def makeFolders():
    os.mkdir('data')
    os.mkdir('data/test')
    os.mkdir('data/train')
    os.mkdir('data/test/cat')
    os.mkdir('data/test/dog')
    os.mkdir('data/train/dog')
    os.mkdir('data/train/cat')