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

import json

from . import _sql, BaseHandler, sendMail




class webhooks(BaseHandler):
	def post(self):
		webhook = json.loads(self.request.body)
		print(json.dumps(webhook, indent=4))
		print "======================"
		print "author:", webhook['commits'][0]['author']['username']
		print "added:", webhook['commits'][0]['added']
		print "modified:", webhook['commits'][0]['modified']

		edits = webhook['commits'][0]['added'] + webhook['commits'][0]['modified']

		for edit in edits:
			print edit
			if '.json' in edit:
				print "Tady je nejaky upraveny modul :)"

		self.write("ACK")