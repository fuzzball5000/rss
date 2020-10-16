import time
import ast
import json

ser = serial.Serial(

    port='/dev/tty.usbserial-14120',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

feed_name = sys.argv[1]
url = sys.argv[2]


rssPR = feedparser.parse(url)
rssCheck = feedparser.parse(url)

rssDataList = []

for index, item in enumerate(rssPR.entries):
    rssDataList.append([item.published, item.title,item.description])

feed = {}
fluff=0

for i in rssDataList:
    entry = "\n".join([str(x) for x in i])
    ihash=hashlib.md5(entry.encode())
    feed.update({ihash.hexdigest():entry})
    fluff=fluff+1

hashin = open('/Users/grichardson/hashes','r+')
newhash  = ''.join(line.rstrip('\r\n') for line in hashin)


for key,value in feed.items():
    if key not in newhash:
        hashin.write(key+'\n')
        ser.write('* * * * * * * * * * * * * * * * * *'.encode())
        ser.write('\n'.encode())
        ser.write(('\n'+value).encode())
        ser.write('\n'.encode())
        ser.write('\n'.encode())
        ser.write('\n'.encode())
    else:
        continue

hashin.close()

