from random import randrange
from mod.fct.mod_gl import *
from mod.fct.mod_math import CoSinus, DISTANCE
from gen_particules import Gen_particules

class Sphere:
	accelere = False

	def __init__(__, boss, coords, speeds=(1, 1, 50), rayon=4):
		__.boss = boss
		__.destroy = False
		__.x, __.y, __.z = coords
		__.angle, __.r = __.x, __.y
		__.xs, __.ys, __.zs = speeds
		__.rayon  = rayon
		__.gen = Gen_particules(100,
							couleur_min=(240, 0, 0), couleur_max=(255, 0, 0),
							taille_min=1, taille_max=5,
							speed_min=(-10, -10, -10), speed_max=(10, 10, 10),
							alpha_min=150, perte_max=2,
							lim_x=(-K.largeur_mapH2, K.largeur_mapH2),
							lim_y=(-K.largeur_mapV2, K.largeur_mapV2),
							lim_z=(0, K.longueur_map))

	def draw(__):
		if not __.destroy:
			if K.mode_cylindre:
				__.angle = (__.angle + __.xs) % 360
				temp = __.r + __.ys
				if 2 + __.rayon  <= temp < K.largeur_mapH2 - __.rayon : __.r = temp
				elif temp < 2 + __.rayon : __.r = 2 + __.rayon; __.ys = - __.ys
				else: __.r = K.largeur_mapH2 - __.rayon; __.ys = - __.ys
				cos, sin = CoSinus(__.angle)
				__.x = cos * __.r
				__.y = sin * __.r
			else:
				tempc = __.x + __.xs
				templ = K.largeur_mapH2 - __.rayon
				if - templ <= tempc <= templ: __.x = tempc
				else:
					__.xs = - __.xs
					if - templ > tempc: __.x = -templ
					else: __.x = templ

				tempc = __.y + __.ys
				templ = K.largeur_mapV2 - __.rayon
				if - templ <= tempc <= templ: __.y = tempc
				else:
					__.ys = - __.ys
					if - templ > tempc: __.y = -templ
					else: __.y = templ
			__.z += __.zs - K.joueur.v
			if __.z < -__.rayon : __.z = - __.rayon
			elif __.z > K.longueur_map * 2: __.z = K.longueur_map * 2
			__.zs += K.joueur.vadd * (1 + 9 * __.accelere)
			if randrange(100) == 50: __.accelere = not __.accelere
			temp = __.x, __.y, __.z
			__.gen.set_coords(temp, temp)
			glPushMatrix()
			glTranslatef(__.x, __.y, __.z)
			glScalef(__.rayon , __.rayon , __.rayon )
			glCallList(__.boss.liste_sphere)
			glPopMatrix()
			for tir in K.tir:
				if __.z + __.rayon   >= tir.z and __.z - __.rayon   <= tir.z + tir.longueur and\
					DISTANCE(__.x, __.y, tir.x, tir.y) <= __.rayon + tir.longueur:
					__.gen.reinit_particules()
					tir.destroy = __.destroy = True
					break
		else:
			if __.gen.particules:
				for i in __.gen.particules: i.z -= K.joueur.v/10.
				__.gen.draw()
