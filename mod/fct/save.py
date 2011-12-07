#-*- coding:cp1252 -*-
from os import mkdir
from mod.fct.mod_file import get_name_without_ext

dic_keys = ["score", "distance", "vmax", "vm", "vie"]

def save_score(dic, filename):
	score = file(filename, "wb")
	for i in range(len(dic_keys)):
		score.write("%d:%d:%f:%f:%d\n" %
		            (dic[dic_keys[i]][0], dic[dic_keys[i]][1], dic[dic_keys[i]][2], dic[dic_keys[i]][3], dic[dic_keys[i]][4]))
	score.close()
	
def verify_score(joueur, dic, filename):
	liste = (joueur.score, joueur.distance, joueur.vmax, joueur.vm, joueur.vie)
	for i in range(len(liste)):
		if dic[dic_keys[i]][i] < liste[i] or \
				dic[dic_keys[i]][i] == liste[i] and sum(dic[dic_keys[i]]) < sum(liste):
			dic[dic_keys[i]] = liste
	save_score(dic, filename)

def line_in_list(line):
	line = line.split(':')
	for i in range(len(line)):
		if 2 <= i <= 3: line[i] = float(line[i])
		else: line[i] = int(line[i])
	return (line)
	
def put_file_in_dict(filename):
	default = [0, 0, 0, 0, 0]
	dic = {"score" : default, "distance" : default, "vmax" : default, "vm" : default, "vie" : default}
	try:
		score = file(filename, "rb")
		for i, line in enumerate(score):
			dic[dic_keys[i]] = line_in_list(line[ : -1])
		score.close()
	except: pass
	return (dic)

def save_highscore(joueur, mod, map):
	try: mkdir("data/scores")
	except: pass
	filename = get_mappath(map, mod)
	dic = put_file_in_dict(filename)
	verify_score(joueur, dic, filename)

def get_mappath(mapname, mod):
	mapname = get_name_without_ext(mapname)
	return ("data/scores/" + str(mod) + mapname + ".jhs")
