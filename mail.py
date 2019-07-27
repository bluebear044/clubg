#!/usr/bin/python
# -*- coding: utf-8  -*-
import config

import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def mail(from_user, from_pwd, to_user, subject, text):
    msg = MIMEText(text)
 
    msg['From'] = from_user
    msg['To'] = to_user
   
    if subject is not "":
        msg['Subject'] = subject
    else:
        msg['Subject'] = "No Title"
 
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(from_user, from_pwd)
    mailServer.sendmail(from_user, to_user, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.quit()

if __name__ == "__main__":
    from_user = config.PRJ_CONFIG['email_id']
    from_pwd = config.PRJ_CONFIG['email_pw']
    to_user = config.PRJ_CONFIG['to_email_id']
    subject = datetime.today().strftime("%Y%m%d%H%M%S") 
    text = sys.argv[1]
    mail(from_user, from_pwd, to_user, subject, text)
