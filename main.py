import requests
from pymongo import MongoClient
import os
import sys
import fileinput
import initialization

# initialization.getWNID('n02084071')
# initialization.deleteNullStrings('n02084071_id.txt')
client = MongoClient('localhost', 27017)
db = client.test
collection = db.users
print(collection.find_one())
# initialization.getWNID('n02121620')
# initialization.deleteNullStrings('n02121620_id.txt')

url = 'http://farm1.static.flickr.com/228/499699798_d5cbf79377.jpg'
r = requests.get(url)
print(r.status_code) 
print(r.url)
if(url == r.url):
    out = open('img.jpg', 'wb')
    out.write(r.content)