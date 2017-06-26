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
        #print help(tornado.locale.get())
        print tornado.locale.get("es_LA")
        #print help(tornado.locale.get().get_closest(['cs','en']))
        print tornado.locale.get('cs_CZ', 'cs_CZ')
        for x in tornado.locale.get_supported_locales():
            print x
        print tornado.locale.get_supported_locales()
        login = self.get_secure_cookie("login")
        token = self.get_secure_cookie("token")
        if not login:
            return None
        else:
            return _sql("SELECT * from Users WHERE login = '%s'" %(login))[0]

    '''
    def get_user_locale(self):
        if not self.get_cookie("locale"):
            self.set_cookie("locale","en_US")
            return "en_US"

        return self.get_cookie("locale")
    '''


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