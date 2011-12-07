from mod.fct.mod_gl import *
from random import randint


class Gen_particules:
	def __init__(__, nombre, regenere=False,
				coords_min=(0, 0, 0), coords_max=(0, 0, 0),
				speed_min=(-100, -100, -100), speed_max=(100, 100, 100),
				couleur_min=(0, 0, 0), couleur_max=(255, 255, 255),
				taille_min=2, taille_max=10,
				alpha_min=1, alpha_max=255,
				perte_min=1, perte_max=254,
				gravite_min=(0, 0, 0), gravite_max=(0, 0, 0),
				lim_x=(), lim_y=(), lim_z=()):

		__.regenere = regenere
		__.nombre = nombre

		__.set_coords(coords_min, coords_max)
		__.set_speed(speed_min, speed_max)
		__.set_couleur(couleur_min, couleur_max)
		__.set_taille(taille_min, taille_max)
		__.set_alpha(alpha_min, alpha_max)
		__.set_perte(perte_min, perte_max)
		__.set_gravite(gravite_min, gravite_max)
		__.set_lim_x(lim_x)
		__.set_lim_y(lim_y)
		__.set_lim_z(lim_z)
		__.reinit_particules()

	def reinit_particules(__): __.particules = [__.create_particule(__.Particule) for i in range(__.nombre)]

	def _set_attr3_(__, c_min, c_max, couleur=False):
		c_min, c_max = list(c_min), list(c_max)
		for i in range(3):
			if c_min[i] > c_max[i]: c_min[i], c_max[i] = c_max[i], c_min[i]
			if couleur: c_min[i], c_max[i] = int(c_min[i])%256, int(c_max[i])%256
			else: c_min[i], c_max[i] = int(c_min[i]), int(c_max[i])
		return [c_min, c_max]

	def _set_alpha_(__, Min, Max):
		Min, Max = int(Min)%256, int(Max)%256
		if not int(Min): Min = 1
		if Min > Max: Min, Max = Max, Min
		return [Min, Max]

	def _set_lim_(__, lim):
		lim = list(lim)
		if lim:
			if len(lim) == 1:
				if lim[0] < 0: lim.append(0)
				elif lim[0] > 0: lim.insert(0, 0)
				else: lim = []
			else:
				if lim[0] > lim[1]: lim.reverse()
				elif lim[0] == lim[1]: lim = []
		else: lim = []
		return lim

	def set_taille(__, Min, Max):
		Min, Max = int(Min), int(Max)
		if not int(Min): Min = 1
		if Min > Max: Min, Max = Max, Min
		__.taille = [Min, Max]

	def set_alpha(__, Min, Max): __.alpha = __._set_alpha_(Min, Max)
	def set_perte(__, Min, Max): __.perte = __._set_alpha_(Min, Max)

	def set_lim_x(__, lim): __.lim_x = __._set_lim_(lim)
	def set_lim_y(__, lim): __.lim_y = __._set_lim_(lim)
	def set_lim_z(__, lim): __.lim_z = __._set_lim_(lim)

	def set_coords(__, Min, Max): __.coords = __._set_attr3_(Min, Max)
	def set_speed(__, Min, Max): __.speed = __._set_attr3_(Min, Max)
	def set_gravite(__, Min, Max): __.gravite = __._set_attr3_(Min, Max)
	def set_couleur(__, Min, Max): __.couleur = __._set_attr3_(Min, Max, True)


	def create_particule(__, particule):
		return particule(
			(
				randint(__.coords[0][0], __.coords[1][0]),
				randint(__.coords[0][1], __.coords[1][1]),
				randint(__.coords[0][2], __.coords[1][2])
			),
			(
				randint(__.speed[0][0], __.speed[1][0])/10.,
				randint(__.speed[0][1], __.speed[1][1])/10.,
				randint(__.speed[0][2], __.speed[1][2])/10.
			),
			(
				randint(__.couleur[0][0], __.couleur[1][0]),
				randint(__.couleur[0][1], __.couleur[1][1]),
				randint(__.couleur[0][2], __.couleur[1][2])
			),
			randint(__.taille[0], __.taille[1]),
			randint(__.alpha[0], __.alpha[1]),
			randint(__.perte[0], __.perte[1]),
			(
				randint(__.gravite[0][0], __.gravite[1][0])/10.,
				randint(__.gravite[0][1], __.gravite[1][1])/10.,
				randint(__.gravite[0][2], __.gravite[1][2])/10.
			)
		)

	def draw(__):
		glEnable(GL_BLEND)
		glDisable(GL_DEPTH_TEST)
		for i in __.particules:
			i.draw()
			if i.alpha:
				if __.lim_x:
					if not (__.lim_x[0] < i.x < __.lim_x[1]): i.alpha = 0
				if i.alpha and __.lim_y:
					if not (__.lim_y[0] < i.y < __.lim_y[1]): i.alpha = 0
				if i.alpha and __.lim_z:
					if not (__.lim_z[0] < i.z < __.lim_z[1]): i.alpha = 0
			if not i.alpha:
				if __.regenere: __.create_particule(i.__init__)
				else: __.particules.remove(i)
		glColor4ub(255, 255, 255, 255)
		glDisable(GL_BLEND)
		glEnable(GL_DEPTH_TEST)

	class Particule:
		liste =  glGenLists(1000)
		glNewList(liste, GL_COMPILE)
		glBegin(GL_POINTS)
		glVertex(0, 0, 0)
		glEnd()
		glEndList()

		def __init__(__, coords, speed=(10, 10, 10), couleur=(255, 255, 255), taille=2, alpha=255, perte=1, gravite=(0, 0, 0)):
			__.x, __.y, __.z = coords
			__.xs, __.ys, __.zs = speed
			__.xg, __.yg, __.zg = gravite
			__.r, __.v, __.b = couleur
			__.taille = taille
			__.alpha = alpha
			__.perte = perte

		def draw(__):
			glPointSize(__.taille)
			glPushMatrix()
			glColor4ub(__.r, __.v, __.b, __.alpha)
			glTranslatef(__.x, __.y, __.z)
			glCallList(__.liste)
			glPopMatrix()
			__.xs += __.xg
			__.ys += __.yg
			__.zs += __.zg
			__.x += __.xs + __.xg
			__.y += __.ys + __.yg
			__.z += __.zs + __.zg
			__.alpha -= __.perte
			if __.alpha < 0: __.alpha = 0
