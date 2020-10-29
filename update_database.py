#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import MySQLdb as mdb


def text_btw(text, start, end, reverse = False):
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
        return ""


def text_btw_replace(text, start, end, replace):
    try:

        num_s = text.index( start )+len(start)
        num_e = text.find(end)
        print num_s, num_e

        text_pre = text[:num_s]
        text_post= text[num_e:]
        out = (text_pre+replace+text_post)
        return out

    except Exception, e:
        return text


mlab_rep = os.path.expanduser("~/repos/Modules/")
#db = sqlite3.connect('MLABdb.db')
#cursor = db.cursor()

db = mdb.connect('localhost', 'root', 'root', 'MLAB')
cur = db.cursor()


for root, dirs, files in os.walk(mlab_rep):
    for file in files:
        if file.endswith('README.md'):
            root_head, root_tail = os.path.split(root)
            readme = open(os.path.join(root, file), 'r').read()

            name = text_btw(readme, "<!--- Name:", ":")
            author = text_btw(readme, "<!--- Author:", ":")
            email = text_btw(readme, "<!--- AuthorEmail:", ":")
            Tags = text_btw(readme, "<!--- Tags:", ":").split('|')
            LongName = text_btw(readme, "<!--- LongName --->", "<!--- ELongName --->")
            lead = text_btw(readme, "<!--- Lead --->", "<!--- ELead --->")
            Description = text_btw(readme, "<!--- Description --->", "<!--- EDescription --->")
            Content = text_btw(readme, "<!--- Content --->", "<!--- EContent --->")
            leadImg = text_btw(readme, "![LeadImg](", ")")

            #lead = ""

            try:
                #cur.execute("INSERT INTO module (name, long_name_en, description_en, author, directory) VALUES('%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE id=id;" %(name, LongName, lead, author, root_head))
                cur.execute("REPLACE INTO module (name, long_name_en, description_en, author, directory) VALUES('%s', '%s', '%s', '%s', '%s');" %(name, LongName, lead, author, root_head))
                #cur.execute("REPLACE INTO module SET name = '%s', long_name_en = '%s', description_en = '%s', author = '%s', directory = '%s';" %(name, LongName, lead.rstrip(), author, root_head))
                #cur.execute("UPDATE module SET name = '%s', long_name_en = '%s', description_en = '%s', author = '%s', directory = '%s';" %(name, LongName, lead.rstrip(), author, root_head, name))
                cur.execute("SELECT id FROM module WHERE name = '%s';" %(name))
                module_id = cur.fetchone()[0]
                cur.execute("DELETE FROM module_tag WHERE id_module = '%s';" %(module_id))
                for tag in Tags:
                    try:
                        cur.execute("SELECT id FROM tags WHERE name = '%s';" %(tag))
                        tag_id = cur.fetchone()[0]
                        print tag_id, module_id
                        cur.execute("INSERT INTO module_tag (id_module, id_tag) VALUES('%s', '%s') ON DUPLICATE KEY UPDATE id=id;" %(module_id, tag_id))

                    except Exception, e:
                        print e
                        print "2>>>> ERR", root, name
            except Exception, e:
                print e
                print "1>>>> ERR", root, name


db.commit()
db.close()


