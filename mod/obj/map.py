from mod.fct.mod_gl import *
from fog import Fog
from random import randrange
from mod.interpreteur import Interpreteur

class Map:
	sphere = None

	def __init__(__, boss, largeurH=50, largeurV=50, longueur=300,
				grav_change=False, no_grav=True, grav=1, grav_dir=0, filename="map/tranche double.bex"):
		__.boss = boss
		__.Interp = Interpreteur()
		if not filename: filename = "map/random.bex"
		__.Interp.start(__, filename)
		__.list_couleur_map = [(0, 0, 0), (0, 65, 65), (0, 65, 0), (65, 65, 0), (65, 0, 0), (65, 0, 65)]
		__.lim_couleur_map = len(__.list_couleur_map)
		__.index_couleur_map = 0

		__.list_couleur_line = [(255, 255, 255), (255, 0, 0), (255, 0, 255), (0, 0, 255), (0, 255, 255), (0, 255, 0)]
		__.lim_couleur_line = len(__.list_couleur_map)
		__.index_couleur_line = 0

		__.list_couleur_bloc = [(0, 205, 205), (0, 205, 0), (205, 205, 0), (205, 0, 0), (205, 0, 205), (205, 205, 205)]
		__.lim_couleur_bloc = len(__.list_couleur_bloc)
		__.index_couleur_bloc = 0

		__.list_couleur_fog = [(0, 115, 115), (0, 115, 0), (115, 115, 0), (115, 0, 0), (115, 0, 115), (115, 115, 115)]
		__.lim_couleur_fog = len(__.list_couleur_fog)
		__.index_couleur_fog = 0

		K.no_grav = no_grav
		K.grav = grav
		K.grav_dir = grav_dir
		K.mode_cylindre = False
		K.bloc = True
		__.fog = Fog(end=longueur, density=0, couleur=(0, 50, 0), alpha = 255)
		__.fog.draw()

		__.create_map(longueur, largeurH, largeurV)
		import bloc
		reload(bloc)
		__.bloc = bloc
		import sphere
		reload(sphere)
		__.mod_sphere = sphere
		__.sphere = []
		__.nbr_ligne = K.longueur_map / 100
		__.i = 100
		K.obj = []
		K.tir = []
		__.creer = False
		__.distance = 0
		__.temps = 0
		__.lim = 0

		__.liste_cube = glGenLists(1)
		glNewList(__.liste_cube, GL_COMPILE)
		draw_pave(1, 1, 1, couleur=())
		glEndList()

		__.liste_cylindre = glGenLists(1)
		glNewList(__.liste_cylindre, GL_COMPILE)
		quadric = gluNewQuadric()
		gluQuadricDrawStyle(quadric, GLU_FILL)
		gluCylinder(quadric, 1, 1, 1, 20, 1)
		gluDisk(quadric, 0, 1, 20, 1)
		glPushMatrix()
		glTranslated(0, 0, 1)
		gluDisk(quadric, 0, 1, 20, 1)
		glPopMatrix()
		gluDeleteQuadric(quadric)
		glEndList()

		__.liste_sphere = glGenLists(1)
		glNewList(__.liste_sphere, GL_COMPILE)
		quadric = gluNewQuadric()
		gluQuadricDrawStyle(quadric, GLU_FILL)
		gluSphere(quadric, 1, 20, 20)
		gluDeleteQuadric(quadric)
		glEndList()

	def create_map(__, longueur=0, largeurH=0, largeurV=0):
		if longueur: K.f = K.longueur_map = longueur
		if largeurH: K.largeur_mapH2 = largeurH
		if largeurV: K.largeur_mapV2 = largeurV
		K.f = longueur
		__.fog.end = K.f

		__.liste_pave_map = glGenLists(1)
		glNewList(__.liste_pave_map, GL_COMPILE)
		draw_rect((-K.largeur_mapH2, -K.largeur_mapV2, 0), (K.largeur_mapH2, -K.largeur_mapV2, 0),
				(K.largeur_mapH2, -K.largeur_mapV2, K.f), (-K.largeur_mapH2, -K.largeur_mapV2, K.f))
		draw_rect((-K.largeur_mapH2, K.largeur_mapV2, 0), (K.largeur_mapH2, K.largeur_mapV2, 0),
				(K.largeur_mapH2, K.largeur_mapV2, K.f), (-K.largeur_mapH2, K.largeur_mapV2, K.f))
		draw_rect((K.largeur_mapH2, -K.largeur_mapV2, 0), (K.largeur_mapH2, K.largeur_mapV2, 0),
				(K.largeur_mapH2, K.largeur_mapV2, K.f), (K.largeur_mapH2, -K.largeur_mapV2, K.f))
		draw_rect((-K.largeur_mapH2, -K.largeur_mapV2, 0), (-K.largeur_mapH2, K.largeur_mapV2, 0),
				(-K.largeur_mapH2, K.largeur_mapV2, K.f), (-K.largeur_mapH2, -K.largeur_mapV2, K.f))
		draw_rect((-K.largeur_mapH2, -K.largeur_mapV2, K.f), (-K.largeur_mapH2, K.largeur_mapV2, K.f),
				(K.largeur_mapH2, K.largeur_mapV2, K.f), (K.largeur_mapH2, -K.largeur_mapV2, K.f))
		glEndList()

		__.liste_cylindre_map = glGenLists(1)
		glNewList(__.liste_cylindre_map, GL_COMPILE)
		glPushMatrix()
		quadric = gluNewQuadric()
		gluQuadricDrawStyle(quadric, GLU_FILL)
		gluCylinder(quadric, K.largeur_mapH2, K.largeur_mapH2, K.f, 40, 1)
		gluCylinder(quadric, 0.9, 0.9, K.f, 40, 1)
		glTranslatef(0, 0, K.f)
		gluDisk(quadric, 0, K.largeur_mapH2, 40, 1)
		gluDeleteQuadric(quadric)
		glPopMatrix()
		glEndList()

		__.liste_pave_ligne = glGenLists(1)
		glNewList(__.liste_pave_ligne, GL_COMPILE)
		glLineWidth(5)
		glBegin(GL_LINES)
		glVertex3i(-K.largeur_mapH2, -K.largeur_mapV2, 0)
		glVertex3i(K.largeur_mapH2, -K.largeur_mapV2, 0)
		glVertex3i(K.largeur_mapH2, K.largeur_mapV2, 0)
		glVertex3i(-K.largeur_mapH2, K.largeur_mapV2, 0)
		glVertex3i(K.largeur_mapH2, -K.largeur_mapV2, 0)
		glVertex3i(K.largeur_mapH2, K.largeur_mapV2, 0)
		glVertex3i(-K.largeur_mapH2, -K.largeur_mapV2, 0)
		glVertex3i(-K.largeur_mapH2, K.largeur_mapV2, 0)
		glEnd()
		glEndList()

		__.liste_cylindre_ligne = glGenLists(1)
		glNewList(__.liste_cylindre_ligne, GL_COMPILE)
		quadric = gluNewQuadric()
		gluQuadricDrawStyle(quadric, GLU_FILL)
		temp = K.largeur_mapH2 - 2
		gluCylinder(quadric, temp, temp, 5, 40, 1)
		gluCylinder(quadric, 1, 1, 5, 40, 1)
		gluDeleteQuadric(quadric)
		glEndList()
		K.f += 1


	def draw(__):
		__.fog.draw()
		if __.Interp.mode: __.distance += K.joueur.v
		else: __.temps += K.temps_boucle
		__.Interp.lire()
		if K.end and K.obj: K.obj = []

		__.i = (__.i - K.joueur.v10) % (K.longueur_map + 1)

		r = __.list_couleur_map[__.index_couleur_map][0]
		v = __.list_couleur_map[__.index_couleur_map][1]
		b = __.list_couleur_map[__.index_couleur_map][2]
		glColor3ub(r*bool(r>0), v*bool(v>0),b*bool(b>0))
		if K.mode_cylindre: glCallList(__.liste_cylindre_map)
		else: glCallList(__.liste_pave_map)
		__.fog.couleur = (__.list_couleur_fog[__.index_couleur_fog][0],
								__.list_couleur_fog[__.index_couleur_fog][1],
								__.list_couleur_fog[__.index_couleur_fog][2])

		for i in range(__.nbr_ligne):
			glColor3ub(__.list_couleur_line[__.index_couleur_line][0],
							__.list_couleur_line[__.index_couleur_line][1],
							__.list_couleur_line[__.index_couleur_line][2])
			glPushMatrix()
			glTranslatef(0, 0, (__.i - i*100) % (K.longueur_map + 1))
			if K.mode_cylindre: glCallList(__.liste_cylindre_ligne)
			else: glCallList(__.liste_pave_ligne)
			glPopMatrix()

		r = __.list_couleur_bloc[__.index_couleur_bloc][0]
		v = __.list_couleur_bloc[__.index_couleur_bloc][1]
		b = __.list_couleur_bloc[__.index_couleur_bloc][2]
		glColor4ub(r*bool(r>0), v*bool(v>0), b*bool(b>0), 255)
		for obj in K.obj: obj.draw()
		for tir in K.tir: tir.draw()
		if K.mode_jeu == 1:
			glColor3ub(255, 0, 0)
			if not __.sphere:
				__.sphere.append(__.mod_sphere.Sphere(__, (0, 0, 50)))
				__.len_sphere = len(__.sphere)
			else:
				nbr_destroy = 0
				for i in __.sphere:
					i.draw()
					if i.destroy: nbr_destroy += 1
				if nbr_destroy == __.len_sphere: K.end = True
