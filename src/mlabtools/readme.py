#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

import jinja2
from jinja2 import Template
from jinja2 import Undefined
    


class readme():
    def __init__(self, filename):
        self.latex_jinja_env = jinja2.Environment(
            block_start_string = '\BLOCK{',
            block_end_string = '}',
            variable_start_string = '\VAR{',
            variable_end_string = '}',
            comment_start_string = '\#{',
            comment_end_string = '}',
            line_statement_prefix = '%-',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
            loader= jinja2.FileSystemLoader(os.path.abspath('.'))
        )
        #sys.setdefaultencoding('utf-8')


        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7"
        self.run(os.path.abspath(filename))



    def text_btw(self, text, start, end, reverse = False):
        try:
            if not reverse:
                num_s = text.index( start ) + len( start )
                text = text[num_s:]
                num_e = text.find(end)
                return text[:num_e].decode('utf8')
            elif reverse:
                num_e = text.find(end)
                text = text[:num_e]
                num_s = text.index( start ) + len( start )
                return text[num_s:].decode('utf8')

        except Exception, e:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 2"
            print e, start, end
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 2"
            return ""


    def text_btw_replace(self, text, start, end, replace):
        try:
            #print "######################################################  1"
            #print text
            num_s = text.index( start )+len(start)
            num_e = text.find(end)
            print num_s, num_e

            text_pre = text[:num_s]
            #print "###################################################### 2"
            #print "PRE"
            #print text_pre
            text_post= text[num_e:]
            #print
            #print "post"
            #print text_post
            #print "###################################################### 3"
            out = (text_pre+replace+text_post)
            #print out
            #print "###################################################### 4"

            return out
        except Exception, e:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 1"
            print e, start, end, replace
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 1"
            return text

    def replace_relativ_imgs(self, text):
        replacement = self.text_btw(text, '![relImg](', ')')
        #print '![relImg]('+replacement+')<!--- '
        #fig = self.text_btw(text, '![relImg]('+replacement+')<!--- ', '--->')
        print "@@@@@@@@@@@@@@@@@2", replacement, folder+'/'+replacement
        out = self.text_btw_replace(text, '![relImg](', ")", folder+'/'+replacement)
        out = out.replace('relImg', '', 1)
        return out

    def md_tex(self, md):
        try:
            proc = subprocess.Popen( ['pandoc', '-f', 'markdown', '-t', 'latex'],stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            proc.stdin.write(md.encode('utf8'))
            proc.stdin.close()
            out = proc.stdout.read().decode('utf8')
            proc.wait()
            return out
        except Exception, e:
            return "Err ----"


    def run(self, filename):

        folder = os.path.dirname(filename)
        project = os.path.basename(folder)

        print filename
        print folder
        print project
        os.chdir(folder)


        readme = open(filename, 'r').read()


        name = self.text_btw(readme, "<!--- Name:", ":")
        author = self.text_btw(readme, "<!--- Author:", ":")
        email = self.text_btw(readme, "<!--- AuthorEmail:", ":")
        LongName = self.text_btw(readme, "<!--- LongName --->", "<!--- ELongName --->")
        lead = self.text_btw(readme, "<!--- Lead --->", "<!--- ELead --->")
        Description = self.text_btw(readme, "<!--- Description --->", "<!--- EDescription --->")
        Content = self.text_btw(readme, "<!--- Content --->", "<!--- EContent --->")
        leadImg = self.text_btw(readme, "![LeadImg](", ")")

        #if leadImg != "":
        leadImg = leadImg
        #else:
        #    leadImg = False

        qr = 'DOC/SRC/img/'+name+'_QRcode.png'

        #leadImg = "/home/roman/repos/newMLAB/test-mlab-repos/Modules/Sensors/SHT31V01A/DOC/SRC/img/SHT31V01A_top_big.jpg"


        Description = self.md_tex(Description)



        schema  ='''
        # Scheme
        '''

        Content = self.text_btw_replace(Content, '<!--- scheme --->', '<!--- Escheme --->', schema)
        Content = self.md_tex(Content)
        Content = Content.replace('label{scheme}', ' \includegraphics[angle=90,origin=c,width=\\textwidth-1cm]{SCH_PCB/SHT31V01A.pdf}')

        print Content

        print lead
        proc = subprocess.Popen( ['pandoc', '-f', 'markdown', '-t', 'latex'],stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(lead.encode('utf8'))
        proc.stdin.close()
        lead = proc.stdout.read().decode('utf8')
        print "#### LEAD #################"
        print lead
        proc.wait()



        Description = self.md_tex(Description)



        print name, author, email, LongName
        #print lead
        #print Description
        #print Content



        #t = latex_jinja_env(leader=open('template.tex').read().decode('utf8'))



        latex_jinja_env = jinja2.Environment(
            block_start_string = '\BLOCK{',
            block_end_string = '}',
            variable_start_string = '\VAR{',
            variable_end_string = '}',
            comment_start_string = '\#{',
            comment_end_string = '}',
            line_statement_prefix = '%-',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
            loader= jinja2.FileSystemLoader(os.path.abspath('/'))
        )



        t = latex_jinja_env.get_template('/home/roman/repos/test-mlab-ui/src/mlabtools/template.tex')
        out = t.render(name = name, author = author, LongName = LongName, email = email, lead=lead, leadImg = leadImg, Description = Description, Content = Content, qr=qr)



        f = open(folder+'/'+name+'.tex', 'w')
        f.write(out.encode('utf8'))
        f.close()
        print 'pdflatex', folder+'/'+name+'.tex', '-interaction=batchmode  -file-line-error', '-output-directory=/home/roman/out/dir', '-aux-directory=/home/roman/out/aux', '-job-name=', name+'.pdf'
        proc = subprocess.Popen(['pdflatex', folder+'/'+name+'.tex', '-interaction=batchmode  -file-line-error', '-output-directory=/home/roman/out/dir', '-aux-directory=/home/roman/out/aux', '-job-name=', name+'.pdf'])
        proc.wait()
        proc = subprocess.Popen(['pdflatex', folder+'/'+name+'.tex', '-interaction=batchmode  -file-line-error', '-output-directory=/home/roman/out/dir', '-aux-directory=/home/roman/out/aux', '-job-name=', name+'.pdf'])
        proc.wait()

        for file in [name+'.log',name+'.aux',name+'.tex',name+'.tex',name+'.toc',name+'.out']:
            try:
                os.remove(file)
            except OSError:
                pass

        name = 'out'
        for file in [name+'.log',name+'.aux',name+'.tex',name+'.tex',name+'.toc',name+'.out',name+'.pdf']:
            try:
                os.remove(file)
            except OSError:
                pass

        #proc = subprocess.Popen(['pdflatex', folder+'/'+'out.tex', '-o', folder+'/'+'README.pdf'])
        #proc.wait()


if __name__ == '__main__':
    readme(sys.argv[1])