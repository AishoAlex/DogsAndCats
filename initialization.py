'''
    Получим здесь нужные нам файлы: 
    с wnid и соответственные списки картинок
'''
import fileinput
import requests
def getWNIDCollection():
    r = requests.get('http://image-net.org/archive/gloss.txt')
    fileName = 'wnid.txt'
    file = open(fileName, 'w', encoding = "utf-8")
    file.write(r.text)
    file.close()
def getWNID(wnid):
    url = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid='+wnid
    r = requests.get(url)
    fileName = wnid+'_id.txt'
    file = open(fileName, 'w', encoding = "utf-8")
    file.write(r.text)
    file.close()
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