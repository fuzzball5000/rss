#!/usr/bin/python

import feedparser
import time
import sys
import serial
import hashlib
import time

ser = serial.Serial(

    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

feed_name = sys.argv[1]
url = sys.argv[2]


rssPR = feedparser.parse(url)
lasthash = str(hashlib.md5(rssPR.entries[0].link + rssPR.entries[0].title))

rssCheck = feedparser.parse(url)

rssDataList = []

for index, item in enumerate(rssPR.entries):
    rssDataList.append([item.published.encode('utf-8'), item.title.encode('utf-8'),item.description.encode('utf-8')])

feed = {}
fluff=0

for i in rssDataList:
    ihash=hashlib.md5(rssPR.entries[fluff].link + rssCheck.entries[fluff].title)
    fluff=fluff+1
    feed.update({ihash.hexdigest():', '.join(i)})

hashin = open('/home/gary/rss/hashes','a+')

for key,value in feed.items():
    if not any(key == line.rstrip('\r\n') for line in hashin):
        hashin.write(key+'\n')
        ser.write('* * * * * * * * * * * * * * * * * *'+'\n')
        ser.write('\n')
        ser.write("%s" % (value))
        ser.write('\n')
        ser.write('\n')
        ser.write('\n')
    else:
        continue

hashin.close()

