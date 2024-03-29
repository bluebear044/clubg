#!/usr/bin/python
# -*- coding: utf-8  -*-
import config

from mail import mail
from logutil import fileLog

import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class Soup:

    def reqUrl(self, url):
        data = requests.get(url, verify=False)
        html = data.text.encode('utf-8')
        return html

    def sendEmail(self, content):
        mail(config.PRJ_CONFIG['email_id'],
            config.PRJ_CONFIG['email_pw'],
            config.PRJ_CONFIG['to_email_id'],
            "Notification : {}".format(datetime.today().strftime("%Y%m%d%H%M%S")),
            ''.join(content))

    def main(self):
        html = self.reqUrl(config.PRJ_CONFIG['request_url'])
        soup = BeautifulSoup(html, 'html.parser')
        banners = soup.find_all(class_='item ing animation_scale_back')
        #yesterday = datetime.today() - timedelta(days=1)
        #yesterdayNum = int(yesterday.strftime('%Y%m%d'))
        checkResult = False
        contentList = []
        linkList = []

        for item in banners:

            contentList.append(config.PRJ_CONFIG['base_url'] + item.get('href').replace('..',''))
            linkList.append(config.PRJ_CONFIG['base_url'] + item.get('href').replace('..',''))

            divs = item.findAll('div')

            item_name = divs[1].find('p', class_='name').get_text()
            item_price = divs[1].find('p', class_='price').get_text()
            item_text = divs[2].find('p', class_='text').get_text()
            
            contentList.append(item_name)
            contentList.append(item_text)
            contentList.append(item_price)

            '''	
        	regex = re.compile(r'\d\d\d\d/\d\d/\d\d')
        	matchobj = regex.search(item.text)
        	reserveDate = matchobj.group()
        	reserveNum = int(reserveDate.replace("/",""))

        	print(yesterdayNum)
        	print(reserveNum)
        	if yesterdayNum <= reserveNum :
        		checkResult = True
        	'''

            contentList.append('\n')

        fName = os.path.join(config.PRJ_CONFIG['path'], "data.txt")
        #print('data path: {}'.format(fName))
        if os.path.exists(fName):

            with open(fName, 'r') as f:
                try:
                    fileList = f.read().splitlines()
                except :
                    print('File Read Exception Occurred')

            if fileList:
                compList = set(fileList) & set(linkList)
                if (len(compList) == len(set(fileList)) and len(compList) == len(set(linkList))):
                    print("Already exists")
                    checkResult = False
                else:
                    checkResult = True
            else:
                checkResult = True

        else :
            checkResult = True

        print("linkList : {}".format(len(linkList)))
        print("checkResult : {}".format(checkResult))
        if linkList and checkResult:

            # Write newest link to file
            with open(fName, 'w') as f:
                try:
                    for data in linkList:
                        f.write(data + '\n')
                    f.close()
                except IOError as e:
                    print('File Write Exception Occurred')
                    print("I/O error({0}): {1}".format(e.errno, e.strerror))
            
            # Send E-Mail
            content = [n + '\n' for n in contentList]
            self.sendEmail(content)

            result = len(linkList)
            print("Mail Send!! " + str(result) + " items")
            fileLog("Mail Send!!")
        else:
            result = 0
            print("Mail Not Send!!")
            fileLog("Mail Not Send!!")

        return result

if  __name__ =='__main__':
    soup = Soup()
    soup.main()
