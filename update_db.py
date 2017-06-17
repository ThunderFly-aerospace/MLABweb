



import os
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         db='MLAB',
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
cursorobj = connection.cursor()


# toto projde vsechny slozky a pokud obsahuje prj info, tak to zapise do DB ...
'''
or top, dirs, files in os.walk('/home/roman/repos/Modules'):
    if "PrjInfo.txt" in files:
        module = os.path.basename(top)
        root = top[26:]
        #print os.path.basename(top), top[26:]
        print module, root
        #cursorobj.execute("UPDATE `MLAB`.`Modules` SET `root` = '%s', `longname_cs`='%s', `longname_en`='%s', `short_cs`='%s', `short_en`='%s', `name` = '%s';" 
        #   %(root, module, module, module, module, module))
        cursorobj.execute("INSERT INTO `MLAB`.`Modules` (`name`, `root`, `longname_cs`, `longname_en`) VALUES ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE `name` = '%s';" %(os.path.basename(top), top[26:], os.path.basename(top), os.path.basename(top), module))
        connection.commit()
'''

# toto projde Moduly v db a priradi je to k zakladnim kategoriim

cursorobj.execute("SELECT * FROM `MLAB`.`Modules`;")
result = cursorobj.fetchall()
for module in result:
    print module['id'], module['name'], module['root'].split('/')[0]

    try:
       
        cursorobj.execute('''
                                INSERT INTO `MLAB`.`module_to_category` (`module`, `category`)
                                VALUES
                                (
                                    (SELECT Modules.id as 'mod_id' FROM MLAB.Modules WHERE Modules.name = '%s'),
                                    (SELECT Categories.id as 'cat_id' FROM MLAB.Categories WHERE Categories.default_root = '%s')
                                );
                            ''' %(module['name'], module['root'].split('/')[0]))
        connection.commit()

    except Exception as e:
        print repr(e)
   




connection.close()
