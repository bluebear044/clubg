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

def soup():
    data = requests.get(config.PRJ_CONFIG['request_url'])
    html = data.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    banners = soup.find_all(class_='reserve_ban')
    #yesterday = datetime.today() - timedelta(days=1)
    #yesterdayNum = int(yesterday.strftime('%Y%m%d'))
    checkResult = False
    contentList = []
    linkList = []

    for item in banners:
	
	   #print(item)
    	
        print(config.PRJ_CONFIG['base_url'] + item.find('a').get('href'))
    	contentList.append(config.PRJ_CONFIG['base_url'] + item.find('a').get('href'))
        linkList.append(config.PRJ_CONFIG['base_url'] + item.find('a').get('href'))
    	
    	#print(item.find('img').get('src'))
        	#contentList.append(item.find('img').get('src'))
        	
    	spans = item.findAll('span')
    	for span in spans:
    	    print(span.text.encode('utf-8'))
    	    contentList.append(span.text)
        
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

    	print('\n')
    	contentList.append('\n')

    fName = config.PRJ_CONFIG['path'] + "data.txt"
    if os.path.exists(fName):

        # 사이트의 비정상 동작으로 잘못 크롤링 된 경우 빈 파일이 생기게 되는데, 이후 제대로 크롤링 되었을때 빈파일이 있는 경우에 동작하도록 방어코딩  
        with open(fName, 'r') as f:
            try:
                if len(f.readlines()) == 0 :
                    checkResult = True
            except :
                print('File Read Exception Occurred')

        with open(fName, 'r') as f:
            try:
                while True:
                    line = f.readline()
                    if not line:
                        break

                    linkSet = set(linkList)
                    if line.strip() in linkSet:
                        print("Already exists")
                    else :
                        print("Not exists")
                        checkResult = True
            except :
                print('File Read Exception Occurred')
    else :
        checkResult = True

    print("linkList : " + str(len(linkList)))
    print("checkResult : " + str(checkResult))
    if len(linkList) != 0 & checkResult == True :

        # Write newest link to file
        with open(fName, 'w') as f:
            try:
                for data in linkList:
                    f.write(data.encode("utf-8") + '\n')
                f.close()
            except IOError as e:
                print('File Write Exception Occurred')
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
        
        # Send E-Mail
	    content = [n.encode('utf-8')+'\n' for n in contentList]
        mail(config.PRJ_CONFIG['email_id'], config.PRJ_CONFIG['email_pw'], config.PRJ_CONFIG['to_email_id'], "Notification : " + datetime.today().strftime("%Y%m%d%H%M%S"), ''.join(content))
    	print("Mail Send!!")
        fileLog("Mail Send!!")

    else :
        print("Mail Not Send!!")
    	fileLog("Mail Not Send!!")


if __name__ == "__main__":
    soup()

