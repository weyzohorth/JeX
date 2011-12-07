from tir import Tir

class Tir_bloc(Tir):
	def create_gen(__): pass

	def draw(__):
		if not __.destroy:
			__.z += __.speed
			if 0 <= __.z <= K.longueur_map + 4 * __.longueur:
				glPushMatrix()
				glTranslatef(__.x, __.y, __.z)
				glScalef(__.largeur, __.largeur, __.longueur)
				glRotated(180, 0, 1, 0)
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
