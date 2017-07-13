



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

'''

# toto projde Moduly v db a priradi je to k zakladnim kategoriim

cursorobj.execute("SELECT * FROM `MLAB`.`Modules`;")
result = cursorobj.fetchall()
for module in result:
    print module['id'], module['name'], module['root'].split('/')[0]

    try:
       
        cursorobj.execute("""
                                INSERT INTO `MLAB`.`module_to_category` (`module`, `category`)
                                VALUES
                                (
                                    (SELECT Modules.id as 'mod_id' FROM MLAB.Modules WHERE Modules.name = '%s'),
                                    (SELECT Categories.id as 'cat_id' FROM MLAB.Categories WHERE Categories.default_root = '%s')
                                );
                            """ %(module['name'], module['root'].split('/')[0]))
        connection.commit()

    except Exception as e:
        print repr(e)
'''


'''
#toto projde PrjInfo.txt soubory a ziska zakladni popisy modulu

for top, dirs, files in os.walk('/home/roman/repos/Modules'):
    if "PrjInfo.txt" in files:
        module = os.path.basename(top)
        file = top+"/PrjInfo.txt"
        data = open(file, 'r').read()
        #print os.path.basename(top), top[26:]
        print module
        print ""

        short_cs = None
        short_en = None
        long_en = None
        long_cs = None
        ust = None
        wiki = None


        try:
            zacatek = data.find('[InfoShortDescription.en]')+27
            if zacatek > 26:
                konec = data[zacatek:].find('[')+zacatek
                short_en = data[zacatek:konec].replace("\r","").replace("\n","").replace("  "," ").replace("  "," ")
                print short_en
        except Exception as e:
            print "neni '[InfoShortDescription.en]"

        try:
            zacatek = data.find('[InfoShortDescription.cs]')+27
            if zacatek > 26:
                konec = data[zacatek:].find('[')+zacatek
                short_cs = data[zacatek:konec].replace("\r","").replace("\n","").replace("  "," ").replace("  "," ")
                print short_cs
        except Exception as e:
            print "neni '[InfoShortDescription.cs]"

        try:
            zacatek = data.find('[InfoLongDescription.en]')+25
            if zacatek > 24:
                konec = data[zacatek:].find('[')+zacatek
                long_en = data[zacatek:konec].replace("\r","").replace("\n","").replace("  "," ").replace("  "," ")
                print long_en
        except Exception as e:
            print "neni '[InfoLongDescription.en]"

        try:
            zacatek = data.find('[InfoLongDescription.cs]')+25
            if zacatek > 24:
                konec = data[zacatek:].find('[')+zacatek
                out = data[zacatek:konec]
                long_cs = data[zacatek:konec].replace("\r","").replace("\n","").replace("  "," ").replace("  "," ")
                print long_cs
        except Exception as e:
            print "neni '[InfoLongtDescription.cs]"

        try:
            zacatek = data.find('[InfoBuyUST]')+13
            if zacatek > 12:
                konec = data[zacatek:].find('[')+zacatek
                ust = data[zacatek:konec]
                print data[zacatek:konec]
        except Exception as e:
            print "neni '[ust]"

        try:
            zacatek = data.find('[WIKI]')+7
            if zacatek > 6:
                konec = data[zacatek:].find('[')+zacatek
                wiki = data[zacatek:konec]
                print data[zacatek:konec]
        except Exception as e:
            print "neni '[wiki]"

        try:
            cursorobj.execute("UPDATE `MLAB`.`Modules` SET `longname_cs`='%s', `longname_en`='%s', `short_cs`='%s', `short_en`='%s', `ust`='%s' WHERE `name` = '%s';" 
                %(short_cs, short_en, long_cs, long_en, ust, module))
            #cursorobj.execute("INSERT INTO `MLAB`.`Modules` (`name`, `root`, `longname_cs`, `longname_en`) VALUES ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE `name` = '%s';" %(os.path.basename(top), top[26:], os.path.basename(top), os.path.basename(top), module))
            connection.commit()
        except:
            pass


connection.close()
'''


for top, dirs, files in os.walk('/home/roman/repos/Modules'):
    if 'jpg' in files.lower() or 'png' in files.lower():
        if files != files.lower():
            print files
