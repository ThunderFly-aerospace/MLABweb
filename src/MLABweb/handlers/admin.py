
#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado
import json
import glob
#from tornado import web
from tornado import ioloop
from tornado import auth
from tornado import escape
from tornado import httpserver
from tornado import options
from tornado import web
from git import Repo

from . import _sql, BaseHandler, sendMail
import hjson



class home(BaseHandler):
    def get(self):
        self.render("index.hbs",  _sql=_sql, parent=self)

class module_detail(BaseHandler):
    def get(self, module = None):
        print module
        #self.write("ahoj")
        module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))[0]
        self.render("modules.detail.hbs", _sql=_sql, module=module, module_data=module_data, images = glob.glob("/home/roman/repos/Modules/"+module_data['root']+"/DOC/SRC/img/*"))

class modules(BaseHandler):
    def get(self, category = None):
        print category
        self.render("modules.hbs",  _sql=_sql, parent=self, category = category)

class module_edit(BaseHandler):
    def get(self, module=None):
        module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))
        if len(module_data) > 0:
            module_data = module_data[0]
        else:
            module_data = None
        print module_data
        self.render("modules.edit.hbs",  parent=self, module_data=module_data, images = glob.glob("/home/roman/repos/Modules/"+module_data['root']+"/DOC/SRC/img/*"))

    def post(self, module=None):
        print "POST: module_edit"
        #print module
        data = self.request.arguments
        #print "##################################################33"

        print json.dumps(self.request.arguments, sort_keys=True, indent=4)
        dotaz = "UPDATE `MLAB`.`Modules` SET `wiki`='%s', `ust`='%s', `longname_cs`='%s', `longname_en`='%s', `short_cs`='%s', `short_en`='%s', `doc_cs`='%s', `doc_en`='%s', image = '%s', status = '%s' WHERE `name`='%s';"  %(self.get_argument('wiki'), self.get_argument('ust'), self.get_argument('longname_cs'), self.get_argument('longname_en'), self.get_argument('short_cs'), self.get_argument('short_en'), self.get_argument('doc_cs'), self.get_argument('doc_en'), self.get_argument('image'), self.get_argument('status'), self.get_argument('name'))
        #print dotaz
        module_data = _sql(dotaz) 

        data_json = {}

        for element in data:
            data_json[element] = data[element][0]

        print ""
        print '/home/roman/repos/Modules/'+self.get_argument('root')+'/module.json'
        print json.dumps(data_json, indent=4)


        with open('/home/roman/repos/Modules/'+self.get_argument('root')+'/module.json', 'w') as out:
            json.dump(data_json, out, indent=4)

        repo = Repo('/home/roman/repos/Modules')
        repo.index.add([self.get_argument('root')])



