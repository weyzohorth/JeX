from interpreteur import Interpreteur
from mod.fct.mod_file import get_allfiles, file_exists, get_ext
from os import remove, rename

def binarise_all():
	"""compresse legerement les fichiers jex en bex, ecrase les anciens bex et supprime les jex source"""
	Inter = Interpreteur()
	for fichier in get_allfiles("../"*bool(__name__ == "__main__")+"map/"):
		path_file = ".".join(fichier.split(".")[:-1])
		if get_ext(fichier) == "jex":
			if file_exists(path_file+".bex") and file_exists(path_file+".jex"): remove(path_file+".bex")
			if not file_exists(path_file+".bex"):
				Inter.binarise(fichier)
				remove(fichier)

def binarise_one(name):
	Inter = Interpreteur()
	fichier = "../"*bool(__name__ == "__main__")+"map/" + name
	path_file = ".".join(fichier.split(".")[:-1])
	if get_ext(fichier) == "jex":
		if file_exists(path_file+".bex") and file_exists(path_file+".jex"): remove(path_file+".bex")
		if not file_exists(path_file+".bex"):
			Inter.binarise(fichier)
			remove(fichier)

def debinarise_all():
	"""decompresse les fichiers bex en jex, n'ecrase pas les anciens jex et supprime les bex si jex cree"""
	Inter = Interpreteur()
	for fichier in get_allfiles("../"*bool(__name__ == "__main__")+"map/"):
		path_file = ".".join(fichier.split(".")[:-1])
		if get_ext(fichier) == "bex" and not file_exists(path_file+".jex"):
			rename(Inter.debinarise(fichier), path_file+".jex")
			remove(fichier)

def debinarise_one(name):
	Inter = Interpreteur()
	fichier = "../"*bool(__name__ == "__main__")+"map/" + name
	path_file = ".".join(fichier.split(".")[:-1])
	if get_ext(fichier) == "bex" and not file_exists(path_file+".jex"):
		rename(Inter.debinarise(fichier), path_file+".jex")
		remove(fichier)

if __name__ == "__main__":
	binarise_all()
	#debinarise_all()
	#binarise_one()
	#debinarise_one("random.bex")
