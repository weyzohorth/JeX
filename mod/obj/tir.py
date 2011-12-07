from mod.fct.mod_gl import *
from mod.fct.mod_math import DISTANCE
from gen_particules import Gen_particules

class Tir:
	liste_tir = glGenLists(1)
	glNewList(liste_tir, GL_COMPILE)
	quadric = gluNewQuadric()
	gluQuadricDrawStyle(quadric, GL_FILL)
	glEnable(GL_BLEND)
	glPushMatrix()
	gluCylinder(quadric, 1, 0, 4, 20, 1)
	glTranslated(0, 0, -4)
	gluCylinder(quadric, 1, 1, 4, 20, 1)
	glTranslated(0, 0, -4)
	gluCylinder(quadric, 0, 1, 4, 20, 1)
	glPopMatrix()
	glDisable(GL_BLEND)
	gluDeleteQuadric(quadric)
	glEndList()

	def __init__(__, coords, speed, longueur=2, largeur=1, couleur=(255, 128, 0, 128)):
		K.tir.append(__)
		__.destroy = False
		__.x, __.y, __.z = coords
		__.speed = speed
		__.longueur, __.largeur = longueur, largeur
		__.r, __.v, __.b, __.a = couleur
		__.create_gen()

	def create_gen(__):
		r, v, b, a = __.r - 15,  __.v - 15,  __.b - 15, __.a - 50
		__.gen = Gen_particules(20,
							couleur_min=(r*bool(r >0), v*bool(v >0), b*bool(b >0)), couleur_max=(__.r, __.v, __.b),
							taille_min=1, taille_max=5,
							speed_min=(-10, -10, -10), speed_max=(10, 10, 10),
							alpha_min=(a-1)*bool(a>0)+1, alpha_max=__.a, perte_max=2,
							lim_x=(-K.largeur_mapH2, K.largeur_mapH2),
							lim_y=(-K.largeur_mapV2, K.largeur_mapV2),
							lim_z=(0, K.longueur_map))

	def draw(__):
		if not __.destroy:
			__.z += __.speed
			if 0 <= __.z <= K.longueur_map + 4 * __.longueur:
				glPushMatrix()
				glTranslatef(__.x, __.y, __.z)
				glScalef(__.largeur, __.largeur, __.longueur)
				glColor4ub(__.r, __.v, __.b, __.a)
				glCallList(__.liste_tir)
				glPopMatrix()
				temp = __.x, __.y, __.z
				__.gen.set_coords(temp, temp)
				for obj in K.obj:
					if K.bloc and obj.x + obj.rx2   >= __.x - __.largeur and obj.x - obj.rx2   <= __.x + __.largeur and\
							obj.y + obj.ry2   >= __.y - __.largeur and obj.y - obj.ry2   <= __.y + __.largeur and\
							obj.z + obj.rz2   >= __.z and obj.z - obj.rz2   <= __.z + __.longueur or\
						not K.bloc and obj.z + obj.rz2   >= __.z and obj.z - obj.rz2   <= __.z + __.longueur and\
							DISTANCE(__.x, __.y, obj.x, obj.y) <= obj.r2 + __.largeur:
						__.gen.reinit_particules()
						__.destroy = True
						if K.mode_jeu == 2: obj.vie -= 1
						break
			else: K.tir.remove(__)
		else:
			if __.gen.particules:
				for i in __.gen.particules: i.z -= K.joueur.v/10.
				__.gen.draw()
			else:
				K.tir.remove(__)

