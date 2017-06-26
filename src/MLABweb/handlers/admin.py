
#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado
import json
import glob
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

import re
from six.moves.html_parser import HTMLParser
from xhtml2pdf import pisa 
import StringIO
import pypandoc
from . import _sql, BaseHandler, sendMail
import hjson


class permalink(BaseHandler):
    @asynchronous
    def get(self, module = None):
        print module
        module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))[0]
        self.render("modules.detail.hbs", _sql=_sql, module=module, module_data=module_data, images = glob.glob("/home/roman/repos/Modules/"+module_data['root']+"/DOC/SRC/img/*"))

class home(BaseHandler):
    @asynchronous
    def get(self):
        self.render("index.hbs",  _sql=_sql, parent=self)

class module_detail(BaseHandler):
    @asynchronous
    def get(self, module = None):
        print module
        #self.write("ahoj")
        module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))[0]
        self.render("modules.detail.hbs", _sql=_sql, module=module, module_data=module_data, images = glob.glob("/home/roman/repos/Modules/"+module_data['root']+"/DOC/SRC/img/*"))

class modules(BaseHandler):
    @asynchronous
    def get(self, category = None):
        print "modules"
        print category
        status = None
        if 'status' in self.request.arguments:
            print self.request.arguments['status']
            status = ','.join(self.request.arguments['status'])
        print "status", status

        if category:
            if status:
                print "category_status"
                modules = _sql("SELECT * FROM `MLAB`.`module_to_category` INNER JOIN MLAB.Modules ON Modules.id = module_to_category.module WHERE `category` = (SELECT id from `MLAB`.`Categories` WHERE `Categories`.`name` = '%s' AND status IN (%s) ORDER by name);" %(category, status))
            else:
                print "category_only"
                modules = _sql("SELECT * FROM `MLAB`.`module_to_category` INNER JOIN MLAB.Modules ON Modules.id = module_to_category.module WHERE `category` = (SELECT id from `MLAB`.`Categories` WHERE `Categories`.`name` = '%s' ORDER by name);" %(category))
        else:
            if status:
                modules = _sql("SELECT * FROM Modules WHERE status IN (%s) ORDER by name;" %(status))
            else:
                modules = _sql("SELECT * FROM Modules ORDER by name;")

        self.render("modules.hbs",  _sql=_sql, parent=self, category = category, modules = modules, status = status)

class modules_overview(BaseHandler):
    @asynchronous
    #@tornado.web.authenticated
    def get(self):
        print "modules overview"
        order = self.get_argument('order', 'id')
        modules = _sql("SELECT * FROM Modules ORDER BY %s" %order)
        #modules = _sql("SELECT  Modules.*,  GROUP_CONCAT(Users.name SEPARATOR ',') module_to_user FROM MLAB.Modules RIGHT JOIN module_to_user ON module_to_user.module = Modules.id INNER JOIN Users ON module_to_user.user = Users.id GROUP BY module_to_user.module ORDER BY Module.id;")
        self.render("modules.overview.hbs",  _sql=_sql, parent=self, modules = modules)

class module_edit(BaseHandler):
    @tornado.web.authenticated
    #@asynchronous
    def get(self, module=None):
        module_data = _sql("SELECT * FROM MLAB.Modules WHERE name='%s'" %(module))
        if len(module_data) > 0:
            module_data = module_data[0]
        else:
            module_data = None

        try:
            en = open('/home/roman/repos/Modules/'+module_data['root']+'/README.md').read()
            print en
            print "!!!!!!!!!!!!!!!!!11"
            module_data['longname_en']  = re.findall('\<!--- subtitle ---\>(.*)\<!--- Esubtitle ---\>', en)[0]
            module_data['short_en']  = re.findall('\<!--- description ---\>(.*)\<!--- Edescription ---\>', en)[0]
            print "pouzivam readme #EN"
        except Exception as e:
            print "readmeErrEN", e

        print "traying to open"
        try:
            print module_data['root']
            cs = open('/home/roman/repos/Modules/'+module_data['root']+'/README.cs.md').read()
            print cs
            print "!!!!!!!!!!!!!!!!!11"
            module_data['longname_cs']  = re.findall('\<!--- subtitle ---\>(.*)\<!--- Esubtitle ---\>', cs)[0]
            module_data['short_cs']  = re.findall('\<!--- description ---\>(.*)\<!--- Edescription ---\>', cs)[0]
            print "pouzivam readme #CS"
        except Exception as e:
            print "readmeErrCS", e

        #print module_data
        self.render("modules.edit.hbs",  parent=self, module_data=module_data, images = glob.glob("/home/roman/repos/Modules/"+module_data['root']+"/DOC/SRC/img/*"), _sql=_sql)
    
    @tornado.web.authenticated
    def post(self, module=None):
        print "POST: module_edit"
        data = self.request.arguments
        #print "##################################################33"

        dotaz = "UPDATE `MLAB`.`Modules` SET `wiki`='%s', `ust`='%s', `longname_cs`='%s', `longname_en`='%s', `short_cs`='%s', `short_en`='%s', `doc_cs`='%s', `doc_en`='%s', image = '%s', status = '%s' WHERE `name`='%s';"  %(self.get_argument('wiki'), self.get_argument('ust'), self.get_argument('longname_cs'), self.get_argument('longname_en'), self.get_argument('short_cs'), self.get_argument('short_en'), self.get_argument('doc_cs'), self.get_argument('doc_en'), self.get_argument('image'), self.get_argument('status'), self.get_argument('name'))
        _sql(dotaz) 

        data_json = {}



        for element in data:
            data_json[element] = data[element][0]

        with open('/home/roman/repos/Modules/'+data_json['root']+'/module.json', 'w') as out:
            json.dump(data_json, out, indent=4)

        text_file = open('/home/roman/repos/Modules/'+self.get_argument('root')+'/README.md', "w")
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

        text_file = open('/home/roman/repos/Modules/'+self.get_argument('root')+'/README.cs.md', "w")
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

        #text_file = open('/home/roman/repos/Modules/'+self.get_argument('root')+'/README.cs.md', "w")
        #text_file.write(pypandoc.convert_text(data_json['doc_cs'], 'markdown_github', format='html').encode('utf8'))
        #text_file.close()

        h = HTMLParser()
        html =  """
                <html>
                <head>
                <meta charset="UTF-8">
                <style>

                    html {
                        max-width: 1000px;
                    }

                    h1, h2, h3, h4 {
                        color: #f00;
                        line-height: 1em;
                        font-size: 150%%;
                    }

                    h1 {
                        font-size: 200%%;
                        
                    }

                    h1::before {
                        counter-increment: count-h1;
                        content: counter(count-h1) " ";
                    }

                    h2::before {
                        counter-increment: count-h2;
                        content: counter(count-h1) "." counter(count-h2) " ";
                    }
                    h3:before {
                        counter-increment: count-h3;
                        content: counter(count-h1) "." counter(count-h2) "." counter(count-h3) " ";
                    }

                    #header, p {
                        font-size: 1.2em;
                    }

                    #footer table {
                        width:100%%;
                    }

                    #footer td {
                      width:50%%;
                    }
                    #footer .generated {
                      text-align: right;
                    }


                    /*** Tables ***/
                    table.gridtable , .gridtable td, .gridtable th{
                      border: 1px solid #666;
                      border-collapse: collapse;
                      padding: 4px;
                    }
                    .gridtable th {
                      background-color: #dedede;
                    }
                    table.infotable, .infotable td, .infotable th {
                      border: 1px solid #666;
                      border-collapse: collapse;
                      padding: 2px 2px 0 2px;
                      line-height: 1.2em;
                      vertical-align: top;
                      text-align: left;
                    }
                    table.infotable {
                      width: 100%%;
                    }
                    .infotable th {
                      background-color: #eee;
                    }

                    /*** HEADER ***/
                    #header {
                      border: 1px solid #000;
                      border-collapse: collapse;
                      margin-bottom: 2em;
                      width:100%%;
                      vertical-align: middle;
                      line-height: 1em;
                    }
                    .attribute {
                      font-weight: bold;
                    }
                    #header .logo, #header .logo img {
                      width:100px;
                    }
                    #header table , #header td {
                      border: 1px solid #000;
                      padding: 0.3em;
                      margin-bottom: 0;
                    }


                    @page {
                        size: a4 portrait;
                        margin: 1cm;
                        margin-bottom: 2cm;
                        @frame header_frame {           /* Static frame */
                            -pdf-frame-content: header_content;
                            left: 50pt; right: 50pt; top: 20pt;
                        }
                        @frame content_frame {             /* Content frame 1 */
                            -pdf-frame-content: content_frame;
                            left: 44pt; right: 44pt; top: 90pt; height: 632pt;
                        }
                        
                        @frame footer_frame {           /* Static frame */
                            -pdf-frame-content: footer;
                            left: 2cm;
                            right: 2cm;
                            bottom: 0.5cm;
                            height: 20pt;
                        }
                        @font-face {
                          font-family: Example, "Example Font";
                          src: url(example.ttf);
                        }
                    }

                </style>
                <head>
                <body>

                    <div id="header_content">
                        <img src="http://195.88.142.202/static/logo.png" style="width: 150pt;"> </img>  
                        <span style="width: 150pt;"> </span>  
                        MLAB module SHT
                    </div>
                    
                    <div id="content_frame">
                    %s
                    </div>

                    <div id="footer">
                        <hr>
                        MLAB.cz - page <pdf:pagenumber> of <pdf:pagecount>
                    </div>
                </body>
                </html>

                """ %(h.unescape(data['doc_cs'][0].decode('utf-8')))
        print html

        text_file = open('/home/roman/repos/Modules/'+data['root'][0]+'/DOC/module.html', "w")
        text_file.write(html.encode('utf-8'))
        text_file.close()

        resultFile = open('/home/roman/repos/Modules/'+data_json['root']+'/module.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(
                html.encode('utf-8'),      # the HTML to convert
                dest=resultFile,           # file handle to recieve result
                encoding='utf-8')
        resultFile.close()                 # close output file

        repo = Repo('/home/roman/repos/Modules')

        repo.index.add([self.get_argument('root')])

        if self.current_user:
            author = Actor(self.current_user['login'], self.current_user['email'])
        else:
            author = Actor("Anonymn", "dms@mlab.cz")
        repo.index.commit("[MLABweb] %s %s" %(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), data_json['name']), author=author, committer=author)
        #print repo.index



