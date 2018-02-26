


###
###    tento program projde celou DB a zkontroluje, kde jsou chyby mezi cestou v DB a realnou cestou v repozitari
###



import os
import json
import pymongo



def main():
    db = pymongo.MongoClient("localhost", 27017).MLABweb

    data = db.Modules.find()
    modules_dic = '/data/Modules/'

    print("Nasledujici vypis obsahuje seznam modulu, ktere maji v json souboru spatne nastavenou cestu oproti realne.")


    for dirName, subdirList, fileList in os.walk(modules_dic, topdown=False):
        for fname in fileList:
            if '.json' in fname:
                if os.path.basename(dirName) == fname[:-5]:
                    data = json.load(open(dirName+'/'+fname))
                    #print('%s\t%s  -- %s %s' %(os.path.basename(dirName), fname, dirName[14:], data['root']))
                    if dirName[14:] != data['root']:
                        print(">>>> CHYBA", data.get("name", ''))
                        print(dirName[14:], ">>" ,data['root'])
                        data['root'] = dirName[14:]

                        file_content = json.dumps(data, indent=4, ensure_ascii=False).encode('utf8')
                        with open(dirName+'/'+fname, "w") as text_file:
                            text_file.write(file_content)

                else:
                    print(">>> !! ", dirName, fname)


if __name__ == '__main__':
    main()