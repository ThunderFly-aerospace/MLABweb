#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado
import json
from bson.json_util import dumps

import glob
import glob2
import time
#from tornado import web
from tornado import ioloop
from tornado import auth
from tornado import escape
from tornado import httpserver
from tornado import options
from tornado import web
from tornado.web import asynchronous
from tornado import gen
import git
from git import Repo, Actor
import os

import re
from six.moves.html_parser import HTMLParser
from w3lib.html import replace_entities
from . import _sql, BaseHandler, sendMail
import subprocess


class permalink(BaseHandler):
    @asynchronous
    def get(self, module = None):
        print module
        module_data = self.db_web.Modules.find({"_id": module})[0]
        documents = glob2.glob(tornado.options.options.mlab_repos+module_data['root']+"//**/*.pdf")
        images = glob.glob(tornado.options.options.mlab_repos+module_data['root']+"doc/img/*")
        self.render("modules.detail.hbs", module=module, module_data=module_data, images = images, documents=documents)

class home(BaseHandler):
    @asynchronous
    def get(self, data=None):
        print "HomePage"
        #print tornado.options.options.as_dict()
        #print tornado.options.OptionParser().as_dict()
        #module_data = _sql("SELECT * FROM MLAB.Modules WHERE status='2' ORDER by modif DESC")
        #module_data = _sql("SELECT * FROM `MLAB`.`Modules` WHERE status='2' AND `image` NOT LIKE '%QRcode%' AND CHARACTER_LENGTH(`longname_cs`) > 20 AND `mark` > 45 ORDER BY 'modif' DESC;")
        #print(module_data)
        module_data = self.db_web.Modules.find({ "$and": [ {"$or":[{'status': 2}, {'status':'2'}]}, {'mark': {"$gte": 45}}, {"$where": "this.longname_cs.length > 20"}, {'image':{"$not":re.compile("QRcode")}}]})
        #print(module_data)
        self.render("index.hbs", parent=self, modules = module_data)

class module_detail(BaseHandler):
    @asynchronous
    def get(self, module = None):
        print module
        #self.write("ahoj")
        #module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))[0]
        module_data = self.db_web.Modules.find({"_id": module})[0]
        #print type(module_data)
        #print module_data
        images = glob.glob(tornado.options.options.mlab_repos+module_data['root']+"/doc/img/*")
        #print images
        self.render("modules.detail.hbs", db_web = self.db_web, module=module, module_data=module_data, images = images, documents = glob2.glob(tornado.options.options.mlab_repos+module_data['root']+"//**/*.pdf"))

class module_comapare(BaseHandler):
    @asynchronous
    def get(self, module = None):
        print module, "< compare"
        module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))[0]

        doc_cs = open(tornado.options.options.mlab_repos+module_data['root']+'/doc/src/module.cs.html').read()
        doc_en = open(tornado.options.options.mlab_repos+module_data['root']+'/doc/src/module.en.html').read()
        self.render("modules.compare.hbs", _sql=_sql, module=module, module_data=module_data, doc_cs=doc_cs, doc_en=doc_en)

class categories(BaseHandler):

    def get(self):
        pass
        categories = self.db_web.Category.find()
        self.render("categories.edit.hbs", categories = categories)
    


class modules(BaseHandler):
    def make_list(self, input):
        print input
        if isinstance(input, list): return input
        else: return [input]

    @asynchronous
    def get(self, category = None):
        print "modules"
        print category
        status = None
        if 'status' in self.request.arguments:
            print "STATUS>>>", self.request.arguments['status']
            status = ",".join(self.make_list(self.request.arguments['status']))
            self.set_cookie("status", status)
            statuss = status.split(",")
            status = map(int, statuss)
        else:
            statuss = self.get_cookie('status', "2").split(",")
            status = map(int, statuss)
        status = status + statuss
        print "status", status
        print "category", category


        if category:
            modules = self.db_web.Modules.find({'category[]': [category],
                                                "status":{"$exists":True, "$in": status }}
                                                )#.aggregate([{ "$lookup": {
                                                 #               "from": "Category",
                                                 #               "foreignField": "_id",
                                                 #               "localField": "category[]",
                                                 #               "as": "category[]"
                                                 #             }}
                                                 #])
            #if status:
            #    print "category_status"
            #    modules = self.db_web.Modules.find({'category[]': [category], "status":{"$exists":True, "$in": status }})
            #    #modules = _sql("SELECT * FROM `MLAB`.`module_to_category` INNER JOIN MLAB.Modules ON Modules.id = module_to_category.module WHERE `category` = (SELECT id from `MLAB`.`Categories` WHERE `Categories`.`name` = '%s' AND status IN (%s) ORDER by name);" %(category, status))
            #else:
            #    modules = self.db_web.Modules.find({'category[]': [category]})
            #    print "category_only",
            #    #modules = _sql("SELECT * FROM `MLAB`.`module_to_category` INNER JOIN MLAB.Modules ON Modules.id = module_to_category.module WHERE `category` = (SELECT id from `MLAB`.`Categories` WHERE `Categories`.`name` = '%s' ORDER by name);" %(category))
            #    #modules = self.Modules.find()
            #modules = []
        else:
            modules = self.db_web.Modules.find({"status":{"$exists":True, "$in": status }}) #.sort({"_id": 1})
            #if status:
            #    print "+++++STATUS"
            #    print status, type(status)
            #    #modules = _sql("SELECT * FROM Modules WHERE status IN (%s) ORDER by name;" %(status))
            #    modules = self.db_web.Modules.find({"status":{"$in": status }}) #.sort({"_id": 1})
            #else:
            #    #modules = _sql("SELECT * FROM Modules ORDER by name;")
            #    modules = self.db_web.Modules.find({"status":{"$exists":True}}) #.sort({"_id": 1})
        #print dumps(modules)
        self.render("modules.hbs", parent=self, category = category, modules = modules, status = status, db_web = self.db_web)

class modules_overview(BaseHandler):
    @asynchronous
    #@tornado.web.authenticated
    def get(self):
        print "modules overview"
        order = self.get_argument('order', '_id')
        #modules = _sql("SELECT * FROM Modules ORDER BY %s" %order)
        modules = self.db_web.Modules.find().sort([(order, 1)])
        #modules = _sql("SELECT  Modules.*,  GROUP_CONCAT(Users.name SEPARATOR ',') module_to_user FROM MLAB.Modules RIGHT JOIN module_to_user ON module_to_user.module = Modules.id INNER JOIN Users ON module_to_user.user = Users.id GROUP BY module_to_user.module ORDER BY Module.id;")
        self.render("modules.overview.hbs", parent=self, modules = modules)

class moduleImageUpload(tornado.web.RequestHandler):
    def post(self):

        print self.request.files
        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        print cname
        
        #fh = open(__UPLOADS__ + cname, 'w')
        #fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)

class module_edit(BaseHandler):
    @tornado.web.authenticated
    #@asynchronous
    def get(self, module=None):
        module_data = self.db_web.Modules.find({"_id": module})
        if module_data.count() > 0:
            module_data = module_data[0]
        else:
            module_data = None

        #try:
        #    en = open(tornado.options.options.mlab_repos+module_data['root']+'/README.md').read()

        #    module_data['longname_en']  = re.findall('\<!--- subtitle ---\>(.*)\<!--- Esubtitle ---\>', en)[0]
        #    module_data['short_en']  = re.findall('\<!--- description ---\>(.*)\<!--- Edescription ---\>', en)[0]
        #    print "pouzivam readme #EN"
        #except Exception as e:
        #    print "readmeErrEN", e

        #print "traying to open"
        #try:
        #    print module_data['root']
        #    cs = open(tornado.options.options.mlab_repos+module_data['root']+'/README.cs.md').read()
        #    #print cs
        #    #print "!!!!!!!!!!!!!!!!!11"
        #    module_data['longname_cs']  = re.findall('\<!--- subtitle ---\>(.*)\<!--- Esubtitle ---\>', cs)[0]
        #    module_data['short_cs']  = re.findall('\<!--- description ---\>(.*)\<!--- Edescription ---\>', cs)[0]
        #    print "pouzivam readme #CS"
        #except Exception as e:
        #    print "readmeErrCS", e

        #print module_data
        self.render("modules.edit.hbs",  parent=self, module_data=module_data, images = glob.glob(tornado.options.options.mlab_repos+module_data['root']+"/doc/img/*"), db_web = self.db_web)
    
    def make_list(self, input):
        if isinstance(input, list): return input
        else: return [input]

    @tornado.web.authenticated
    def post(self, module=None):
        print "POST: module_edit"
        print self.request
        data = self.request.arguments


        print data
        #print "##################################################33"
        module = self.get_argument('name').strip()
        
        #dotaz = "UPDATE `MLAB`.`Modules` SET `wiki`='%s', `ust`='%s', `longname_cs`='%s', `longname_en`='%s', `short_cs`='%s', `short_en`='%s', `doc_cs`='%s', `doc_en`='%s', image = '%s', status = '%s', mark = '%s' WHERE `name`='%s';"  
        #%(self.get_argument('wiki').strip(), self.get_argument('ust').strip(),
        #    self.get_argument('longname_cs'), self.get_argument('longname_en'), self.get_argument('short_cs'), self.get_argument('short_en'),
        #    self.get_argument('doc_cs'), self.get_argument('doc_en'), self.get_argument('image').strip(), self.get_argument('status').strip(),
        #    self.get_argument('mark').strip(), self.get_argument('name').strip())
        #_sql(dotaz) 

        self.db_web.Modules.update_one({"_id": self.get_argument('name').strip()},{ "$set":{
            "wiki": self.get_argument('wiki').strip(),
            "ust": self.get_argument('ust').strip(),
            "longname_cs": self.get_argument('longname_cs'),
            "longname_en": self.get_argument('longname_en'),
            "short_cs": self.get_argument('short_cs'),
            "short_en": self.get_argument('short_en'),
            "doc_cs": self.get_argument('doc_cs'),
            "doc_en": self.get_argument('doc_en'),
            "image": self.get_argument('image').strip(),
            "status": int(self.get_argument('status').strip()),
            "mark": float(self.get_argument('mark').strip()),
            "author[]": self.make_list(self.get_arguments('author[]')),
            "category[]": self.make_list(self.get_arguments('category[]'))
        }})

        print self.get_arguments('author[]')
        print self.get_arguments('category[]')

        data_json = {}


        for element in data:
            data_json[element] = data[element][0]


        data_json['category[]'] = self.make_list(data.get('category[]', []))
        data_json['author[]'] = self.make_list(data.get('author[]', []))

        with open(tornado.options.options.mlab_repos+data_json['root']+'/' + module + '.json', 'w') as out:
            json.dump(data_json, out, indent=4)

        '''
        if '.jpg' in data_json['image'] or '.JPG' in data_json['image']:
            #cmd = 'convert /home/roman/repos/Modules/'+data_json['root']+'/'+data_json['image'] +' -sampling-factor 4:2:0 -strip -quality 80 -interlace JPEG -colorspace RGB /home/roman/repos/Modules/'+ data_json['root'] +'/DOC/SRC/img/'+ module +'_title.jpg'
            #print cmd
            #process = subprocess.Popen(cmd)
            process = subprocess.Popen(["convert", "/home/roman/repos/Modules/%s/%s" %(data_json['root'], data_json['image']),"-sampling-factor","4:2:0","-strip","-quality","80","-interlace","JPEG","-colorspace","RGB","/home/roman/repos/Modules/%s/DOC/SRC/img/%s_title.jpg" %(data_json['root'], module)])
            process.wait()
            data_json['image'] = tornado.options.options.mlab_repos+ data_json['root'] +'/DOC/SRC/img/'+ module +'_title.jpg'

            dotaz = "UPDATE `MLAB`.`Modules` SET image = '%s' WHERE `name`='%s';"  %(data_json['image'], module)
            _sql(dotaz) 
        '''

        text_file = open(tornado.options.options.mlab_repos+self.get_argument('root')+'/README.md', "w")
        text_file.write(
            """
[Czech](./README.cs.md)
<!--- module --->
# %(module)s
<!--- Emodule --->

<!--- subtitle --->%(subtitle)s<!--- Esubtitle --->

![%(module)s](%(image)s)

<!--- description --->%(text)s<!--- Edescription --->
            """ %{'module':data_json['name'], 'image':data_json['image'], 'subtitle':data_json['longname_en'], 'text':data_json['short_en']})
        text_file.close()

        text_file = open(tornado.options.options.mlab_repos+self.get_argument('root')+'/README.cs.md', "w")
        text_file.write(
            """
[English](./README.md)
<!--- module --->
# %(module)s
<!--- Emodule --->

<!--- subtitle --->%(subtitle)s<!--- Esubtitle --->

![%(module)s](%(image)s)

<!--- description --->%(text)s<!--- Edescription --->
            """ %{'module':data_json['name'], 'image':data_json['image'], 'subtitle':data_json['longname_cs'], 'text':data_json['short_cs']})
        text_file.close()


        html_content = replace_entities(data_json['doc_cs']).encode('UTF-8')

        html =  """
<html>
<head>
    <meta charset="UTF-8">
    <title>%(module)s</title>
    <meta name="generator" content="pandoc" />
    <meta name="subtitle" content="%(subtitle)s"/>
    <meta name="author" content="%(author)s"/>
    <meta name="TopImage" content="/home/roman/repos/Modules/OpAmps/OZDUAL02B/DOC/SRC/img/OZDUAL02B_Top_Big.JPG"/>
    <meta name="QR" content="/home/roman/repos/Modules/OpAmps/OZDUAL02B/DOC/SRC/img/OZDUAL02B_QRcode.png"/>
    <meta name="abstract" content="%(abstract)s"/>

<style>
</style>
<head>
<body>
    
    %(doc)s

</body>
</html>

                """ %{'module':data_json['name'],'subtitle':data_json['longname_cs'], 'doc':html_content, 'author':"Autor 1, Autor 2", 'abstract':data_json['short_cs']}
        #print html

        #text_file = open(tornado.options.options.mlab_repos+data['root'][0]+'/DOC/SRC/module.cs.html', "w")
        #text_file.write(html)
        #text_file.close()





        html_content = replace_entities(data_json['doc_en']).encode('UTF-8')

        html =  """
<html>
<head>
    <meta charset="UTF-8">
    <title>%(module)s</title>
    <meta name="generator" content="pandoc" />
    <meta name="subtitle" content="%(subtitle)s"/>
    <meta name="author" content="%(author)s"/>
    <meta name="TopImage" content="/home/roman/repos/Modules/OpAmps/OZDUAL02B/DOC/SRC/img/OZDUAL02B_Top_Big.JPG"/>
    <meta name="QR" content="/home/roman/repos/Modules/OpAmps/OZDUAL02B/DOC/SRC/img/OZDUAL02B_QRcode.png"/>
    <meta name="abstract" content="%(abstract)s"/>

<style>
</style>
<head>
<body>
    
    %(doc)s

</body>
</html>

                """ %{'module':data_json['name'],'subtitle':data_json['longname_en'], 'doc':html_content, 'author':"Autor 1, Autor 2", 'abstract':data_json['short_en']}
        #print html

        #text_file = open(tornado.options.options.mlab_repos+data['root'][0]+'/DOC/SRC/module.en.html', "w")
        #text_file.write(html)
        #text_file.close()


        #process = subprocess.Popen(["pandoc", "-s", tornado.options.options.mlab_repos+data['root'][0]+'/DOC/SRC/module.cs.html', "-o", tornado.options.options.mlab_repos+data['root'][0]+'/DOC/'+data_json['name']+'.cs.pdf', "--template=/home/roman/repos/test-mlab-ui/src/MLABweb/template/doc.en.latex"])
        #process = subprocess.Popen(["pandoc", "-s", tornado.options.options.mlab_repos+data['root'][0]+'/DOC/SRC/module.en.html', "-o", tornado.options.options.mlab_repos+data['root'][0]+'/DOC/'+data_json['name']+'.en.pdf', "--template=/home/roman/repos/test-mlab-ui/src/MLABweb/template/doc.en.latex"])
        


        repo = Repo(tornado.options.options.mlab_repos)
        repo.index.add([self.get_argument('root')])

        if self.current_user:
            author = Actor(self.current_user['_id'], self.current_user['email'])
        else:
            author = Actor("Anonymn", "dms@mlab.cz")
        repo.index.commit("[MLABweb] %s %s" %(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), data_json['name']), author=author, committer=author)



