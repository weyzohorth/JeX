from random import randint, random
from mod.fct.mod_math import DISTANCE, DIRECTION, CoSinus
from mod.fct.mod_gl import *

class Bloc:
	sons = [pygame.mixer.Sound("data/sounds/sound/passe"+str(i)+".ogg") for i in range(1,4)]
	son_collision = pygame.mixer.Sound("data/sounds/sound/cogne.ogg")
	for s in sons: s.set_volume(0.5)

	def __init__(__, boss, coords=(), speeds_min=(0, 0, 0), speeds_max=(0, 0, 0),
				rxmin=K.largeur_mapH2/5, rxmax=K.largeur_mapH2/3,
				rymin=K.largeur_mapV2/5, rymax=K.largeur_mapV2/3, rzmin=0, rzmax=0, auto_destruction=False, vie=1):
		K.obj.append(__)
		__.boss = boss
		__.vie_max = vie
		__.vie = vie
		if rxmin > rxmax: rxmin, rxmax = rxmax, rxmin
		elif rxmax == rxmin: rxmax += 1
		if rymin > rymax: rymin, rymax = rymax, rymin
		elif rymax == rymin: rymax += 1
		__.rx_max = int(rxmax)
		__.rx_min = int(rxmin)
		__.ry_max = int(rymax)
		__.ry_min = int(rymin)
		if rzmax: __.rz_max = int(rzmax)
		else: __.rz_max = int(DISTANCE(0, 0, __.rx_max, __.ry_max))
		if rzmin: __.rz_min = int(rzmin)
		else: __.rz_min = int(DISTANCE(0, 0, __.rx_min, __.ry_min))
		if __.rz_min > __.rz_max: __.rz_min, __.rz_max = __.rz_max, __.rz_min
		elif __.rz_max == __.rz_min: __.rz_max += 1
		__.xs_min, __.ys_min, __.zs_min = speeds_min
		__.xs_max, __.ys_max, __.zs_max = speeds_max
		if __.xs_min > __.xs_max: __.xs_min, __.xs_max = __.xs_max, __.xs_min
		if __.ys_min > __.ys_max: __.ys_min, __.ys_max = __.ys_max, __.ys_min
		if __.zs_min > __.zs_max: __.zs_min, __.zs_max = __.zs_max, __.zs_min

		__.coords = coords
		__.len_coords = len(coords)

		__.auto_destruction = auto_destruction

		__.new_coords()

	def new_coords(__):
		__.vie = __.vie_max
		__.collision = False
		__.rx = randint(__.rx_min, __.rx_max)
		__.rx2 = __.rx / 2.
		__.ry = randint(__.ry_min, __.ry_max)
		__.ry2 = __.ry / 2.
		__.rz = randint(__.rz_min, __.rz_max)
		__.rz2 = __.rz / 2.
		__.r2 = DISTANCE(0, 0, __.rx, __.ry) / 2.
		__.xs = randint(__.xs_min, __.xs_max) / 100.
		__.ys = randint(__.ys_min, __.ys_max) / 100.
		__.zs = randint(__.zs_min, __.zs_max) / 100.

		if not __.len_coords or __.len_coords == 1:
			if K.mode_cylindre:
				angle = random() * 360
				temp_min, temp_max = 2 + int(__.ry2),  K.largeur_mapH2 - int(__.ry2)
				if temp_min > temp_max: temp_min, temp_max = temp_max, temp_min
				r_cylindre = randint(temp_min, temp_max)
				cos, sin = CoSinus(angle)
				__.x = cos * r_cylindre
				__.y = -sin * r_cylindre
			else:
				temp = int(K.largeur_mapH2 - __.rx2)
				__.x = randint(-temp, temp)
				temp = int(K.largeur_mapV2 - __.ry2)
				__.y = randint(-temp, temp)
			if __.len_coords == 1: __.z = __.coords[0]
			else: __.z = randint(K.longueur_map+int(__.rz2), K.longueur_map*2-int(__.rz2))
		elif __.len_coords == 3:
			__.x, __.y, __.z = __.coords
		elif __.len_coords == 2:
			__.x, __.y = __.coords
			__.z = randint(K.longueur_map+int(__.rz2), K.longueur_map*2-int(__.rz2))
		__.play = False

	def draw(__):
		jx, jy = K.joueur.x, K.joueur.y
		__.z -= K.joueur.v10 - __.zs
		if __.z > K.longueur_map * 3: __.new_coords()
		if not K.no_grav:
			if K.mode_cylindre:
				r_cylindre = DISTANCE(0, 0, __.x, __.y)
				if r_cylindre  + K.grav < K.largeur_mapH2 - 0.1: r_cylindre += K.grav
				elif r_cylindre >= K.largeur_mapH2: r_cylindre = K.largeur_mapH2
				cos, sin = CoSinus(DIRECTION(0, 0, __.x, __.y) + __.xs)
				__.x = cos * r_cylindre
				__.y = -sin * r_cylindre
			else:
				if K.grav_dir == 0:
					temp = __.ry2 * K.bloc - K.largeur_mapV2 + 0.1
					if __.y - K.grav > temp: __.y -= K.grav
					else: __.y = temp

				elif K.grav_dir == 1:
					temp = -__.rx2 * K.bloc + K.largeur_mapH2 - 0.1
					if __.x + K.grav < temp: __.x += K.grav
					else: __.x = temp

				elif K.grav_dir == 2:
					temp = -__.ry2 * K.bloc + K.largeur_mapV2 - 0.1
					if __.y + K.grav < temp: __.y += K.grav
					else: __.y = temp

				elif K.grav_dir == 3:
					temp = __.rx2 * K.bloc - K.largeur_mapH2 + 0.1
					if __.x - K.grav > temp: __.x -= K.grav
					else: __.x = temp
		if K.mode_cylindre:
			if K.no_grav:
				temp = DISTANCE(0, 0, __.x, __.y) + __.ys
				if 2 + __.r2/2 <= temp <= K.largeur_mapH2 - 0.1: r_cylindre = temp
				elif temp >= K.largeur_mapH2 - 0.1: r_cylindre = K.largeur_mapH2 - 0.1 ; __.ys = -__.ys
				elif temp < 2 + __.r2/2: r_cylindre = 2 + __.r2/2; __.ys = -__.ys
				cos, sin = CoSinus(DIRECTION(0, 0, __.x, __.y) + __.xs)
				__.x = cos * r_cylindre
				__.y = -sin * r_cylindre
		else:
			if K.no_grav or 1 != K.grav_dir != 3:
				temp = - __.rx2 * K.bloc + K.largeur_mapH2 - 0.1
				if - temp <= __.x + __.xs <= temp: __.x += __.xs
				elif - temp > __.x + __.xs: __.x = - temp; __.xs = - __.xs
				elif temp < __.x + __.xs: __.x = temp; __.xs = - __.xs

			if K.no_grav or 0 != K.grav_dir != 2:
				temp = - __.ry2 * K.bloc + K.largeur_mapV2 - 0.1
				if - temp <= __.y + __.ys <= temp: __.y += __.ys
				elif - temp > __.y + __.ys: __.y = - temp; __.ys = - __.ys
				elif temp < __.y + __.ys: __.y = temp; __.ys = - __.ys

		glPushMatrix()
		if K.bloc:
			glTranslatef(__.x-__.rx2, __.y-__.ry2, __.z-__.rz2)
			glScaled(__.rx, __.ry, __.rz)
			glCallList(__.boss.map.liste_cube)
		else:
			glTranslatef(__.x, __.y, __.z)
			glScalef(__.r2, __.r2, __.r2)
			glCallList(__.boss.map.liste_cylindre)
		glPopMatrix()

		if K.joueur.v:
			if not __.collision  and __.z - __.rz2 <= 0 < __.z + __.rz2:
				__.collision_joueur(jx, jy)
				if not __.play:
					dist = DISTANCE(jx, jy, __.x, __.y)
					if dist < 10 + __.r2 or K.joueur.v >= 120: __.sons[2].play()
					elif dist < 20 + __.r2 or K.joueur.v >= 60: __.sons[1].play()
					elif dist < 30 + __.r2: __.sons[0].play()
					__.play = True
			elif __.z + __.rz2 < 0:
				if K.mode_jeu == 2: K.joueur.vie -= 1
				if __.auto_destruction: K.obj.remove(__)
				else:	__.new_coords()

		if K.mode_jeu == 2 and __.vie <= 0:
			K.joueur.score += __.vie_max * (K.joueur.v + K.joueur.accelere) * 10 / (1 + 9 * bool(not K.joueur.accelere))
			if __.auto_destruction: K.obj.remove(__)
			else:	__.new_coords()

	def collision_joueur(__, jx, jy):
		if K.bloc and __.x - __.rx2 < jx < __.x + __.rx2 and __.y - __.ry2 < jy < __.y + __.ry2 or\
				not K.bloc and DISTANCE(__.x, __.y, jx, jy) < __.r2:
			K.joueur.score -= ((180 - K.joueur.v) / 720) * K.joueur.score
			if K.joueur.v > 30: K.joueur.v -= 30
			else: K.joueur.v = 0
			__.accelere = False
			__.collision = True
			K.joueur.vie -= 1
			__.play = True
			if K.joueur.vie: __.son_collision.play()
			else:
				K.joueur.son_panne.play()
				K.joueur.channel_avance.stop()
				pygame.mixer.music.fadeout(5000)
