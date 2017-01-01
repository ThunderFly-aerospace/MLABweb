#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado
#from tornado import web
from tornado import ioloop
from tornado import auth
from tornado import escape
from tornado import httpserver
from tornado import options
from tornado import web

from . import _sql, BaseHandler, sendMail




class webhooks(BaseHandler):
	def post(self):
		webhook = self.request.body
		print webhook
		self.write("ACK")