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
import functools
import json
#import sqlite3
import MySQLdb as mdb
import time
import datetime
import calendar


from handlers import github, admin, auth
from handlers import _sql, BaseHandler, basic


tornado.options.define("port", default=10010, help="port", type=int)
tornado.options.define("debug", default=False, help="debug mode")


class all(BaseHandler):
    def get(self, arg=None):
        #self.write("ACK")
        self.render("index.hbs",  _sql=_sql, parent=self)


    def post(self, arg=None):
        self.write("ACK")


class WebApp(tornado.web.Application):
    def __init__(self, config={}):

        name = 'MLAB'
        server = 'meteor2.astrozor.cz'

        server_url = '{}:{}'.format(server, tornado.options.options.port)

        handlers =[
            (r'/', admin.home),
            (r'/module/(.*)/edit/', admin.module_edit),
            (r'/module/(.*)/edit', admin.module_edit),
            (r'/module/(.*)/compare/', admin.module_comapare),
            (r'/module/(.*)/compare', admin.module_comapare),
            (r'/module/(.*)/', admin.module_detail),
            (r'/module/(.*)', admin.module_detail),
            (r'/module/', admin.modules),
            (r'/module', admin.modules),
            (r'/modules/all', admin.modules_overview),
            (r'/modules/(.*)/', admin.modules),
            (r'/modules/(.*)', admin.modules),
            (r'/modules', admin.modules),
            (r'/admin/', admin.home),
            (r'/admin/module', admin.modules),
            (r'/admin/modules', admin.modules),
            (r'/admin/module/new', all),
            (r'/admin/module/edit(.*)', admin.module_edit),

            (r'/PermaLink/(.*)', admin.permalink),

            (r'/login/oauth/github', auth.O_github),
            (r'/login/newuser', auth.newuser),
            (r'/login/', auth.O_login),
            (r'/login', auth.O_login),
            (r'/logout/', auth.O_logout),
            (r'/logout', auth.O_logout),

            (r'/git/hook', github.webhooks),

            #staticke soubory je vhodne nahradit pristupem primo z proxy serveru. (pak to tolik nevytezuje tornado)
            (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': "/static/"}),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': '/home/roman/repos/test-mlab-ui/src/MLABweb/static/'}),
            (r'/repos/(.*)', tornado.web.StaticFileHandler, {'path': '/home/roman/repos/Modules/'}),
            (r'/git/hook/', github.webhooks),
            (r"/(.*)", all),
        ]
        settings = dict(
            cookie_secret="ROT13IrehaxnWrArwyrcfvQvixnAnFirgr",
            template_path= "/home/roman/repos/test-mlab-ui/src/MLABweb/template/",
            static_path= "/home/roman/repos/test-mlab-ui/src/MLABweb/static/",
            xsrf_cookies=False,
            name=name,
            server_url=server_url,
            site_title=name,
            login_url="/login",
            #ui_modules=modules,
            port=tornado.options.options.port,
            compress_response=True,
            debug=tornado.options.options.debug,
            autoreload=True
        )
        tornado.locale.load_translations("/home/roman/repos/test-mlab-ui/src/MLABweb/locale/")
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebApp())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
    #http_server.start(4)



if __name__ == "__main__":
    main()
