# -*- coding: cp1252 -*-
from fct.mod_gl import *
from fct.mod_base import *
from fct.mod_file import *
from os import remove, getcwd

class Interpreteur:
	"""
		distance # pour signaler que les valeurs précédentes les commandes sont des distances (mode par défaut)
		temps # pour signaler que les valeurs précédentes les commandes sont des temps (en ms)
		cylindre bool # 0 ou 1 desactive active, le mode cylindrique
		mode_bloc bool # 0 ou 1 les blocs sont cylindriques ou en parallèlépipède rectangle
		bloc x y z xsmin xsmax ysmin ysmax zsmin zsmax rxmin rxmax rymin rymax rzmin rzmax auto_destruction # soit x 10 y 5 ou z 50 ou les 3
		couleurs_map int int int (| int int int | int int int)# 0 - 255 r v b séparé par " | " liste des couleurs de la map
		couleurs_line int int int (| int int int | int int int)
		couleurs_bloc int int int (| int int int | int int int)
		couleurs_fog int int int (| int int int | int int int)
		index_couleur_map operateur int # operateur + pour +=, = pour rendre égal et - pour -=
		index_couleur_line operateur int
		index_couleur_fog operateur int
		index_couleur_bloc operateur int
		index_couleurs  operateur int # modifie tous les index_couleur_
		no_grav bool #0 ou 1
		grav float
		grav_dir string #sens de la gravite   bas down | droite right | haut up | gauche left
		map_dimensions int int int # longueur, largeurH, largeurV 0 pour ne pas changer la valeur
		loop_start int #ou oo pour infini
		loop_end #distance est égale à 0, après cet appel
		vitesse operateur float #vitesse du joueur 0 - 180
		vie_max int #nombre de vies maximum du joueur
		vie operateur int #nombre de vies du joueur
		print cmd #affiche la valeur de la commande dans la console

		#largeur_reelle = largeur_donnee  * 2
		#toutes les commandes sont précédées du temps ou de la distance à laquelle elles doivent se produire .
		#exemple:
		#0 temps #dès le départ, l'unite de mesure sera le temps
		#1000 distance # puis une seconde après le départ, l'unite sera la distance
		#10000 couleur_map 255 0 0 # et enfin à 10000 unite (10km) on change la couleur de la map

		#les commandes peuvent etre exécutées légèrement avant, le moment prévu .
		#les indentations sont acceptées avant les distances/temps mais pas après sur la ligne
		#les espaces quand à eux sont interdits, si ce n'est pas pour séparer les éléments d'une ligne de commande .
		# une ligne de commençant pas par un nombre considérée comme un commentaire
		#exemple:
		#0 vie_max 3 #n'est pas un commentaire
		#ceci est un commentaire
		#2_ ceci aussi en est un
	"""
	def start(__, Map, filename):
		__.filename = ""
		if get_ext(filename) == "bex": filename = __.debinarise(filename)
		__.fichier = file(filename)
		__.Map = Map
		__.last_line = __.fichier.readline()
		while not __.test_line(): __.last_line = __.fichier.readline()[:-1]
		__.mode = True
		__.loop = []
		__.seek = 0
		__.seeks_loop = []
		__.index_loop = 0
		__.limite_loop = 0
		__.save_cmd = False
		__.cmd = []
		K.end = False

	def lire(__):
		if not K.end:
			line = __.last_line[:]
			__.limite = int(line.split(" ")[0])
			i = 0
			while i < 10 and (__.mode and __.Map.distance >= __.limite or not __.mode and __.Map.temps >= __.limite):
				i += 1
				__.interprete_line(line[:-1])
				__.seek += len(__.last_line)
				__.last_line = __.fichier.readline()
				if not __.last_line:
					K.end = True
					break
				else:
					while not __.test_line():
						__.seek += len(__.last_line)
						__.last_line = __.fichier.readline()
						if not __.last_line:
							K.end = True
							break
					if not K.end:
						line = __.last_line[:]
						__.limite = int(line.split(" ")[0])
					else: break
			if K.end:
				__.fichier.close()
				if __.filename: __.filename = remove(__.filename)


	def interprete_line(__, string):
		string = string.lower()
		liste = string.split(" ")[1:]
		cmd = liste[0]
		#print "|", string, "|"
		params = liste[1:]
		if cmd == "temps": __.mode = False
		##############################################################################
		elif cmd == "distance": __.mode = True
		##############################################################################
		elif cmd == "cylindre": K.mode_cylindre =  bool(int(params[0]))
		##############################################################################
		elif cmd == "mode_bloc": K.bloc =  bool(int(params[0]))
		##############################################################################
		elif cmd == "no_grav": K.no_grav = bool(int(params[0]))
		##############################################################################
		elif cmd == "grav": K.grav = float(params[0])
		##############################################################################
		elif cmd == "grav_dir":
			sens = params[0].lower()
			if sens == "bas" or sens == "down": K.grav_dir = 0
			elif sens == "droite" or sens == "right": K.grav_dir = 1
			elif sens == "haut" or sens == "up": K.grav_dir = 2
			elif sens == "gauche" or sens == "left": K.grav_dir = 3
		##############################################################################
		elif cmd == "vie_max": K.joueur.vie_max = int(params[0])
		##############################################################################
		elif cmd == "vie":
			if params[0] == "+": K.joueur.vie += int(params[1])
			elif params[0] == "=": K.joueur.vie = int(params[1])
			elif params[0] == "-": K.joueur.vie -= int(params[1])
		##############################################################################
		elif cmd == "vitesse":
			if params[0] == "+":  K.joueur.v += float(params[1])
			elif params[0] == "=": K.joueur.v = float(params[1])
			elif params[0] == "-":K.joueur.v -= float(params[1])
		##############################################################################
		elif cmd.count("index_couleur_"):
			fin_cmd = cmd.split("_")[-1]
			variable = "index_couleur_" + fin_cmd
			valeur = getattr(__.Map, variable)
			limite =  getattr(__.Map, "lim_couleur_" + fin_cmd)
			if params[0] == "+": setattr(__.Map, variable, (valeur + int(params[1])) % limite)

			elif params[0] == "=": setattr(__.Map, variable, int(params[1]) % limite)
			elif params[0] == "-": setattr(__.Map, variable, (valeur - int(params[1])) % limite)
		elif cmd == "index_couleurs":
			for fin_cmd in ["map", "line", "bloc", "fog"]:
				variable = "index_couleur_" + fin_cmd
				valeur = getattr(__.Map, variable)
				limite =  getattr(__.Map, "lim_couleur_" + fin_cmd)
				if params[0] == "+": setattr(__.Map, variable, (valeur + int(params[1])) % limite)

				elif params[0] == "=": setattr(__.Map, variable, int(params[1]) % limite)
				elif params[0] == "-": setattr(__.Map, variable, (valeur - int(params[1])) % limite)
		##############################################################################
		elif cmd == "loop_start":
			if params[0].lower() == "oo" or params[0].lower().count("o"): __.loop.append("oo")
			else: __.loop.append(int(params[0]))
			__.seeks_loop.append(__.seek + len(string) + 1)
			if __.mode: __.Map.distance = 0
			else: __.Map.temps = 0
		##############################################################################
		elif cmd == "loop_end":
			if __.loop[-1]:
				__.fichier.seek(__.seeks_loop[-1])
				__.seek = __.seeks_loop[-1] - len(string) - 1
				if __.loop[-1] > 0 and type(__.loop[-1]) == type(1): __.loop[-1] -= 1
			else:
				__.seeks_loop.pop(-1)
				__.loop.pop(-1)
			if __.mode: __.Map.distance = 0
			else: __.Map.temps = 0
		##############################################################################
		elif cmd.count("couleurs_"):
			fin_cmd = cmd.split("_")[-1]
			liste_params = []
			temp = []
			for p in params:
				if p != "|":
					temp.append(int(p))
				else:
					liste_params.append(tuple(temp))
					temp = []
			if len(temp) == 3: liste_params.append(tuple(temp))
			setattr(__.Map, "list_couleur_" + fin_cmd, liste_params)
			setattr(__.Map, "lim_couleur_" + fin_cmd, len(liste_params))
			setattr(__.Map, "index_couleur_" + fin_cmd, 0)
		##############################################################################
		elif cmd == "map_dimensions": __.Map.create_map(int(params[0]), int(params[1]), int(params[2]))
		##############################################################################
		elif cmd == "bloc":
			dico = {"x": None, "y": None, "z": None, "xsmin": 0, "ysmin": 0, "zsmin": 0, "xsmax": 0, "ysmax": 0, "zsmax": 0,
				"rxmin": K.largeur_mapH2/5, "rxmax": K.largeur_mapH2/3,
				"rymin": K.largeur_mapV2/5, "rymax": K.largeur_mapV2/3, "rzmin": 0, "rzmax": 0, "auto_destruction": False}
			i = 0
			limite = len(params)
			while i + 1< limite:
				dico[params[i]] = int(params[i + 1])
				i += 2
			temp = (__.Map.distance - __.limite) * bool(dico["auto_destruction"])
			if dico["x"] != None and dico["y"] != None and dico["z"] != None: coords = (int(dico["x"]),  int(dico["y"]), int(dico["z"])-temp)
			elif dico["x"] != None: coords = (int(dico["x"]),  int(dico["y"]))
			elif dico["z"] != None: coords = (int(dico["z"])-temp, )
			else: coords = ()
			__.Map.bloc.Bloc(__.Map.boss, coords,
											(dico["xsmin"], dico["ysmin"], dico["zsmin"]),(dico["xsmax"], dico["ysmax"], dico["zsmax"]),
											dico["rxmin"], dico["rxmax"],
											dico["rymin"], dico["rymax"], dico["rzmin"], dico["rzmax"], bool(dico["auto_destruction"]))

		if __.save_cmd and not cmd.count("loop"): __.cmd.append(string)

	def test_line(__):
		try:
			temp = __.last_line.split(" ")
			if len(temp) >= 2:
				int(temp[0])
				return True
		except: pass
		return False

	def debinarise(__, filename):
		__.filename = ".".join(filename.split(".")[:-1])
		if file_exists(__.filename) and get_ext(__.filename) != "jex": remove(__.filename)
		fichier = file(filename, "rb")
		string = base_to_base(fichier.read(), 256, 101, caract_text())
		fichier.close()
		fichier = file(__.filename, "w")
		fichier.write("0"*bool(string[0] == " ")+string)
		fichier.close()
		return __.filename

	def binarise(__, filename):
		if get_ext(filename) != "bex":
			__.filename = try_name(".".join(filename.split(".")[:-1]+["bex"]))
			fichier = file(filename)
			string = base_to_base(fichier.read().replace("\t", "").replace("\n\n\n", "\n").replace("\n\n", "\n").replace("\r\r\r", "\r").replace("\r\r", "\r"), 101, 256, caract_text())
			fichier.close()
			fichier = file(__.filename, "wb")
			fichier.write(string)
			fichier.close()
			return __.filename

if __name__ == "__main__":
	inter = Interpreteur()
	filename = "test.jex"
	if filename: inter.binarise("../map/"+filename)
	#inter.debinarise("../map/test.bex")
