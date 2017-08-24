



import os
import pymysql.cursors
import re
import json
import glob

repos_home = '/home/roman/repos/Modules/'

connection = pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         db='MLAB',
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
cursorobj = connection.cursor()

'''
# toto projde vsechny slozky a pokud obsahuje prj info, tak to zapise do DB ...
for top, dirs, files in os.walk(repos_home):
    if "PrjInfo.txt" in files:
        module = os.path.basename(top)
        root = top[26:]
        #print os.path.basename(top), top[26:]
        print module, root
        print cursorobj.execute("UPDATE `MLAB`.`Modules` SET `root` = '%s', WHERE `name` = '%s';" 
           %(root, module))
        print cursorobj.execute("INSERT INTO `MLAB`.`Modules` (`name`, `root`, `longname_cs`, `longname_en`, `status`) VALUES ('%s', '%s', '%s', '%s', 2) ON DUPLICATE KEY UPDATE `name` = '%s';" %(module, root, os.path.basename(top), os.path.basename(top), module))
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

for top, dirs, files in os.walk(repos_home):
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

'''
for top, dirs, files in os.walk(repos_home):
    #if 'jpg' in files.lower() or 'png' in files.lower():
    #    if files != files.lower():
    #        print files
    #print top
    for file in files:
        #print ">>", file
        if 'module.json' in file:
            print os.path.join(top,file), ">>",
            print os.path.join(top, os.path.basename(top)+'.json')
            os.rename(os.path.join(top,file), os.path.join(top, os.path.basename(top)+'.json') )
'''





#
# prejmenovat slozky (udelat z nich mala pismena)
#
#
dic ={
'PCB_SCH': 'pcb_sch',
'pcb_sch': 'sch_pcb',
'PCB': 'pcb',
'CAM_DOC': 'cam_doc',
'DOC': 'doc',
'CAM': 'cam',
'DATA': 'data',
'CAD': 'cad',
'Python': 'python',
'LIB': 'lib',
'MICROCHIP': 'microchip',
'Arduino': 'Aaduino',
'Text_Prog': 'text_prog',
'Komponenty_upravene': 'komponenty_upravene',
'Doc': 'doc',
'PDF': 'pdf',
'LINUX': 'linux',
'Wiring': 'wiring',
'Utilities': 'utilities',
'Boxes': 'boxes',
'Src': 'src',
'SRC': 'src',
'HTML': 'html',
'FZP': 'fzp',
'Map': 'map',
'Libraries': 'libraries',
'GAL': 'gal',
'ARM': 'arm',
'CCS': 'ccs',
'Debug': 'debug',
'Files': 'files',
'PIN': 'pin',
'PIC': 'pic',
'FLIR': 'flir',
'Project': 'project',
'PragoBoard': 'prago_board',
'CAM_AMA': 'cam_ama',
'SCH_PCB': 'sch_pcb',
'SCH': 'sch',
'AMF': 'amf',
'CAM_PROFI': 'cam_profi',
'AVR': 'avr',
'WIN': 'win',
'SW': 'sw'
}

folders = {}

for top, dirs, files in os.walk(repos_home):
    if not '.git' in top:
        #print top

        folder_parent, folder = os.path.split(top)
        folders[folder] = folder

        if folder in dic:
            print top, " >> ", os.path.join(folder_parent, dic[folder])
            os.rename(top, os.path.join(folder_parent, dic[folder]))


#print folders




'''


#
#       Prejmenuje nazvy souboru  napr LTS01A_Big_Top.JPG na LTS01A_big_top.jpg
#
#



def keymap_replace(
        string, 
        mappings,
        lower_keys=False,
        lower_values=False,
        lower_string=False,
    ):
    """Replace parts of a string based on a dictionary.

    This function takes a string a dictionary of
    replacement mappings. For example, if I supplied
    the string "Hello world.", and the mappings 
    {"H": "J", ".": "!"}, it would return "Jello world!".

    Keyword arguments:
    string       -- The string to replace characters in.
    mappings     -- A dictionary of replacement mappings.
    lower_keys   -- Whether or not to lower the keys in mappings.
    lower_values -- Whether or not to lower the values in mappings.
    lower_string -- Whether or not to lower the input string.
    """
    replaced_string = string.lower() if lower_string else string
    for character, replacement in mappings.items():
        replaced_string = replaced_string.replace(
            character.lower() if lower_keys else character,
            replacement.lower() if lower_values else replacement
        )
    return replaced_string



dic ={
'Top': 'top',
'Small': 'small',
'TOP': 'top',
'SMALL': 'small',
'Big': 'big',
'BIG': 'big',
'Bottom': 'bottom',
'BOTTOM': 'bottom',
'JPG': 'jpg',
'SVG': 'svg',
'PNG': 'png',
'PDF': 'pdf',
'TXT': 'txt'
}


for top, dirs, files in os.walk(repos_home):
    if not '.git' in top:
        #print top
        for file in files:
            print "\t ",  os.path.join(top,file), ">>", os.path.join(top,keymap_replace(file, dic))
            os.rename(os.path.join(top,file), os.path.join(top,keymap_replace(file, dic)))

'''





'''

#
#   zmeni umisteni obrazku z /doc/src/img/ do /doc/img/
#
#

for top, dirs, files in os.walk(repos_home):
    if not '.git' in top:
        #print top

        if 'src/img' in top:
            #print top, ">>", 
            directory = top.replace('/doc/src/img', '/doc/img')
            if not os.path.exists(directory):  os.makedirs(directory)
            for file in files:
                print os.path.join(top,file), ">>", os.path.join(directory, file)
                print file
                os.rename(os.path.join(top,file), os.path.join(top.replace('/doc/src/img', '/doc/img'),file))
            if len(files) == 0:
                print "odstranim", top
                try: 
                    os.rmdir(top)
                except Exception as e:
                    print e


'''



#
#   zmeni umisteni slozek z /sch_pcb /cam_ama, /cam_profi, /cam_doc do /hw/*/
#
#

for top, dirs, files in os.walk(repos_home):
    if not '.git' in top:
        #print top

        if ('/cam_profi' in top or '/sch_pcb' in top or '/cam_ama' in top or '/cam_doc' in top) and not 'hw' in top:
            print top, ">>",
            
            directory = top
            if 'sch_pcb' in top:
                directory = top.replace('/sch_pcb', '/hw/sch_pcb')
            elif 'cam_profi' in top:
                directory = top.replace('/cam_profi', '/hw/cam_profi')
            elif 'cam_ama' in top:
                directory = top.replace('/cam_ama', '/hw/cam_ama')
            elif 'cam_doc' in top:
                directory = top.replace('/cam_doc', '/hw/cam_doc')
            
            if not os.path.exists(directory):  os.makedirs(directory)

            print directory

            
            for file in files:
                print os.path.join(top,file), ">>", os.path.join(directory, file)
                print file
                os.rename(os.path.join(top,file), os.path.join(directory,file))
            if len(files) == 0:
                print "odstranim", top
                try: 
                    os.rmdir(top)
                    pass
                except Exception as e:
                    print e
            


for top, dirs, files in os.walk(repos_home):
    if not '.git' in top:
        #print top

        if ('/pdf' in top ) and not 'doc' in top:
            print top, ">>",
            
            directory = top
            if '/pdf' in top:
                directory = top.replace('/pdf', '/doc/pdf')
            
            if not os.path.exists(directory):  os.makedirs(directory)

            print directory

            
            for file in files:
                print os.path.join(top,file), ">>", os.path.join(directory, file)
                print file
                os.rename(os.path.join(top,file), os.path.join(directory,file))
            if len(files) == 0:
                print "odstranim", top
                try: 
                    os.rmdir(top)
                    pass
                except Exception as e:
                    print e
            

for top, dirs, files in os.walk(repos_home):
    if not '.git' in top:
        for file in files:
            if 'module.en.html' in file or 'module.cs.html' in file or 'module.html' in file:
                print top, file
                os.remove(os.path.join(top, file))
            elif 'module' in file:
                print top, file, files



err_list = []

cursorobj.execute("SELECT * FROM MLAB.Modules")
result = cursorobj.fetchall()
for module in result:
    print ""
    print module['name']
    project_file = os.path.join(repos_home, module['root'], module['name']+'.json')
    project_file_alternative = os.path.join(repos_home, module['root'], 'module.json')
    images =  glob.glob(os.path.join(repos_home, module['root'],"doc/img/*"))

    image = None
    for img in images:
        if 'top_big' in img:
            image = img.replace(os.path.join(repos_home, module['root']), "")
        elif 'QRcode' in img and not image:
            image = img.replace(os.path.join(repos_home, module['root']), "")
    print image

    if image:
        print cursorobj.execute("UPDATE `MLAB`.`Modules` SET `image` = '%s' WHERE `name` = '%s';"  %(image, module['name']))


    if os.path.exists(project_file) and os.path.isfile(project_file):
        print "FILE EXISTS"
        with open(project_file) as data_file:    
            project_param = json.load(data_file)
            porkacovat = True

    elif os.path.exists(project_file_alternative) and os.path.isfile(project_file_alternative):
        print "FILE EXISTS ALTERNATIVE"
        os.rename(project_file_alternative, project_file)
        with open(project_file) as data_file:    
            project_param = json.load(data_file)
            porkacovat = True

    else:
        print "MUSIM SOUBOR VYTVORIT"
        err_list.append(module['name'])
        porkacovat = False
        project_param = {}

    #if porkacovat:
    project_param['wiki'] = module['wiki']
    project_param['image'] = module['image']
    project_param['status'] = module['status']
    project_param['ust'] = module['ust']
    project_param['root'] = module['root']
    project_param['name'] = module['name']
    project_param['short_en'] = module['short_en']
    project_param['short_cs'] = module['short_cs']
    project_param['longname_en'] = module['longname_en']
    project_param['longname_cs'] = module['longname_cs']
    project_param['doc_en'] = module['doc_en']
    project_param['doc_cs'] = module['doc_cs']


    print project_file
    with open(project_file, 'w') as outfile:
        json.dump(project_param, outfile, indent=4)


print err_list

connection.commit()

