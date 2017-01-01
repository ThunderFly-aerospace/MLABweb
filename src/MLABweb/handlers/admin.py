
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




class home(BaseHandler):
    def get(self):
        

        self.render("index.hbs",  _sql=_sql, parent=self)

class modules(BaseHandler):
    def get(self):
        
        self.render("modules.hbs",  _sql=_sql, parent=self)

class module_edit(BaseHandler):
    def get(self, param=None):
        sensor_name = self.get_argument("name", None)

        sensor = _sql("SELECT `id`, `id_category`, `id_directory`, `name`, `long_name_cs`, `long_name_en`, `description_cs`, `description_en`, `id_type`, `date_create` FROM MLAB.module WHERE name = '%s';"%(sensor_name))
        
        self.render("modules.edit.hbs",  _sql=_sql, parent=self, sensor = sensor)