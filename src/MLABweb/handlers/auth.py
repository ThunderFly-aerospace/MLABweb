#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
from tornado import web
from tornado import websocket
from . import _sql, BaseHandler, sendMail
import json
import datetime
import smtplib


import urllib
import urllib2
import requests

from requests_oauthlib import OAuth2Session

class O_logout(BaseHandler):
    def get(self):
        print "odhlasuji TE!!!!!!!!!!!!!!!"
        self.clear_cookie("login")
        self.clear_cookie("token")

        self.redirect("/")


class O_login(BaseHandler):
    def get(self):
        login = self.get_secure_cookie("login", None)
        #token = eval(self.get_secure_cookie("token", None))

        print "###########################"
        print login

        #else:
        github = OAuth2Session("ed66f4255ebebd63b335", scope = ["user:email"])
        authorization_url, state = github.authorization_url('https://github.com/login/oauth/authorize')

        print "redirect", state, authorization_url
        self.redirect(authorization_url)

        #print "redirect"
        #self.redirect('https://github.com/login/oauth/authorize?client_id=%s' %("ed66f4255ebebd63b335"), permanent=True)

class O_github(BaseHandler):

    def get(self):
        print "GitHub"
        github_code = self.get_argument('code', None)
        github = OAuth2Session("ed66f4255ebebd63b335", scope = ["user:email"])
        token = github.fetch_token('https://github.com/login/oauth/access_token', code = github_code, client_secret='44eebca3bf45fa8357731d1c87ceaeb840922a61')
        user_j = github.get('https://api.github.com/user').json()
        email_j = github.get('https://api.github.com/user/emails').json()
        print 'GithubLogin', github_code, user_j, email_j
        user_db=_sql("SELECT count(*) as count FROM Users WHERE login = '%s';" %(user_j['login']))[0]['count']

        print token
        print user_j
        print "------------"

        email = None
        for e in email_j:                   # najdi mail, ktery je primarni
            if e['primary'] == True:
                email = e['email']
            else:
                print "mail vedlejsi", e
        print email


        self.set_secure_cookie('login', user_j['login'])
        self.set_secure_cookie('token', repr(token))

        utcnow = datetime.datetime.utcnow().isoformat()

        if user_db == 1: # uzivatel je zpet :)
            _sql("UPDATE `Users` SET `name` = '%s', `email` = '%s', `service` = '%s', `last_login` = '%s' WHERE login = '%s';" 
                %(user_j['name'], email, "github", utcnow, user_j['login']))
            print "redir /"
            self.redirect("/")

        elif user_db == 0: # Novy uzivatel
            _sql("INSERT INTO `Users` (`login`, `name`, `email`, `service`, `date_joined`, `last_login`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"
                %(user_j['login'], user_j['name'], email, "github", utcnow, utcnow))

            #sendMail("%s<%s>"%(user_j['name'],email),"Welcome to  RTbolidozor", open("/home/roman/repos/RTbolidozor/emails/new_reg","r").read()%(user_j['name']))
            print "novy uzivatel"
            self.redirect("/newuser")

        else:
            print  "Chyba, prosím nahlašte do mailinglistu Bolidozoru č.0003"
            self.write("Chyba, prosím nahlašte do mailinglistu Bolidozoru č.0003")


        #_sql("REPLACE INTO `.`geozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum))
        #self.redirect('https://github.com/login/oauth/authorize?client_id=%s' %("ed66f4255ebebd63b335"), permanent=True)


class newuser(BaseHandler):
    def get(self):
        self.write("Ahoj, <br> Vítáme Vás na stránkách<a href='/'><b> MLAB </b></a> pokračujte na <a href='/'>hlavní stránku</a>")