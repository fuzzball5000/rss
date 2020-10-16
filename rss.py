#!/usr/bin/python

import feedparser
import time
import sys
from escpos.printer import Serial
import hashlib
import time
import ast
import json
import io

print('Boop')

p = Serial(devfile='/dev/tty.usbserial-14120',
           baudrate=9600,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True)

feed_name = sys.argv[1]
url = sys.argv[2]
rssPR = feedparser.parse(url)
rssCheck = feedparser.parse(url)

rssData = {}


for item in rssPR.entries:
    rssData[item.link] = "{}\n{}\n{}\{}\n".format(item.title, item.author, item.published, item.summary)

feed = {}
fluff=0

for i in rssData:
    entry = rssData[i]
    ihash=hashlib.md5(entry.encode())
    feed.update({ihash.hexdigest():entry})
    fluff=fluff+1

hashin = open('/Users/grichardson/hashes','r+')
newhash  = ''.join(line.rstrip('\r\n') for line in hashin)

for key,value in feed.items():
    if key not in newhash:
        
        p.control('LF')
        p.control('LF')
        p.text(value)
        p.control('LF')
        p.control('LF')
        hashin.write(key+'\n')
        
        pass
    else:
        continue

hashin.close()
