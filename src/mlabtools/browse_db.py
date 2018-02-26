


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


	for i, module in enumerate(data):
		filename = modules_dic + module['root'] + '/' + module['_id'] + '.json'
		val = os.path.isfile(filename) 
		if not val:
			print(i, val, module['_id'])



if __name__ == '__main__':
	main()