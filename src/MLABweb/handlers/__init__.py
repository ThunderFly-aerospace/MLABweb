#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

import os
import pymysql.cursors

import tornado
from requests_oauthlib import OAuth2Session

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        login = self.get_secure_cookie("login")
        token = self.get_secure_cookie("token")
        if not login:
            return None
        else:
            return login


def sendMail(to, subject = "MLAB", text = "No content"):
        message="""From:  MLAB distributed measurement systems <dms@mlab.cz>
To: %s
MIME-Version: 1.0
Content-type: text/html
Subject: %s
""" %(to, subject)
        message += text
        print"-----"
        print to
        print message
        print"-----"
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail("MLAB distributed measurement systems <dms@mlab.cz>", to, message )
        smtp.close()




def _sql(query, read=False, db="MLAB"):
        print "#>", query
        #connection = mdb.connect(host="localhost", user="root", passwd="root", db=db, use_unicode=True, charset="utf8", cursorclass=mdb.cursors.DictCursor)
        

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db=db,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            cursorobj = connection.cursor()
            result = None
            cursorobj.execute(query)
            result = cursorobj.fetchall()
            if not read:
                connection.commit()
            connection.close()
            #print "################################"
            #print result
            return result
        except Exception, e:
                print "Err", e
                connection.close()
                return ()