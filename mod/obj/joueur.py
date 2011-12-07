from mod.fct.mod_math import CoSinus, DIRECTION, DISTANCE
from mod.fct.mod_gl import *
from math import atan, pi

class Joueur:
	event_types = [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION,
							pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
	son_avance = pygame.mixer.Sound("data/sounds/sound/avance.ogg")
	son_accelere = pygame.mixer.Sound("data/sounds/sound/accelere.ogg")
	son_panne = pygame.mixer.Sound("data/sounds/sound/panne.ogg")
	channel_avance = pygame.mixer.Channel(0)

	font = pygame.font.Font("data/fonts/lords3.ttf", 32)
	tex_vitesse = surface_to_texture(font.render("vitesse (km/h):", True, pygame.Color(255, 0, 0)))
	tex_vit = surface_to_texture(font.render("10", True, pygame.Color(255, 0, 0)))

	tex_distance = surface_to_texture(font.render("distance (km):", True, pygame.Color(255, 0, 0)))
	tex_dis = surface_to_texture(font.render("0", True, pygame.Color(255, 0, 0)))

	tex_score = surface_to_texture(font.render(": score", True, pygame.Color(255, 0, 0)))
	tex_sco = surface_to_texture(font.render("0", True, pygame.Color(255, 0, 0)))

	tex_degat = surface_to_texture(font.render(": degats", True, pygame.Color(255, 0, 0)))
	tex_deg = surface_to_texture(font.render("[]", True, pygame.Color(255, 0, 0)))

	liste_cokpit = glGenLists(1)
	glNewList(liste_cokpit, GL_COMPILE)
	glEnable(GL_BLEND)
	glBegin(GL_LINES)
	c = 20
	glVertex2f(0, K.h2)
	glVertex2f(K.w2-c, K.h2)
	glVertex2f(K.w2+c, K.h2)
	glVertex2f(K.w, K.h2)

	glVertex2f(K.w2, 0)
	glVertex2f(K.w2, K.h2-c)
	glVertex2f(K.w2, K.h2+c)
	glVertex2f(K.w2, K.h)

	c += c
	glVertex2f(K.w2+c, K.h2+c)
	glVertex2f(K.w2+c, K.h2-c)
	glVertex2f(K.w2-c, K.h2-c)
	glVertex2f(K.w2-c, K.h2+c)
	glVertex2f(K.w2+c, K.h2-c)
	glVertex2f(K.w2-c, K.h2-c)
	glVertex2f(K.w2+c, K.h2+c)
	glVertex2f(K.w2-c, K.h2+c)
	glEnd()

	x_rect = 150
	y_rect = 150
	h_rect = 40
	w_rect = 200
	glDisable(GL_BLEND)

	glColor3ub(255, 255, 255)
	draw_rect_tex((0, 0, 0), (x_rect, y_rect, 0), (x_rect, y_rect+h_rect, 0), (0, h_rect*2, 0), tex_vitesse)
	draw_rect_tex((x_rect, y_rect, 0), (x_rect+w_rect, y_rect, 0), (x_rect+w_rect, y_rect+h_rect, 0), (x_rect, y_rect+h_rect, 0), tex_vit)

	draw_rect_tex((0, K.h-h_rect*2, 0), (x_rect, K.h-(y_rect+h_rect), 0), (x_rect, K.h-y_rect, 0), (0, K.h, 0), tex_distance)
	draw_rect_tex((x_rect, K.h-(y_rect+h_rect), 0), (x_rect+w_rect, K.h-(y_rect+h_rect), 0),
						(x_rect+w_rect, K.h-y_rect, 0), (x_rect, K.h-y_rect, 0), tex_dis)

	draw_rect_tex((K.w-x_rect, y_rect, 0),
						(K.w-0.1, 0, 0),
						(K.w-0.1, h_rect*2, 0),
						(K.w-x_rect, y_rect+h_rect, 0), tex_score)
	draw_rect_tex((K.w-(x_rect+w_rect), y_rect, 0),
						(K.w-x_rect, y_rect, 0),
						(K.w-x_rect, y_rect+h_rect, 0),
						(K.w-(x_rect+w_rect), y_rect+h_rect, 0), tex_sco)

	draw_rect_tex((K.w-x_rect, K.h-(y_rect+h_rect), 0),
						(K.w, K.h-h_rect*2, 0),
						(K.w, K.h, 0),
						(K.w-x_rect, K.h-y_rect, 0), tex_degat)
	draw_rect_tex((K.w-(x_rect+w_rect), K.h-(y_rect+h_rect), 0),
						(K.w-x_rect, K.h-(y_rect+h_rect), 0),
						(K.w-x_rect, K.h-y_rect, 0),
						(K.w-(x_rect+w_rect), K.h-y_rect, 0), tex_deg)
	glEndList()

	liste_point = glGenLists(1)
	glNewList(liste_point, GL_COMPILE)
	glEnable(GL_BLEND)
	glBegin(GL_POINTS)
	glVertex2f(0, 0)
	glEnd()
	glDisable(GL_BLEND)
	glEndList()

	#x_rect = 150
	#y_rect = 150
	#h_rect = 40
	#w_rect = 200
	liste_line_haut = glGenLists(1)
	glNewList(liste_line_haut, GL_COMPILE)
	glEnable(GL_BLEND)
	glBegin(GL_LINES)
	glVertex2f(x_rect+w_rect, K.h-y_rect-2)
	glVertex2f(K.w-(x_rect+w_rect), K.h-y_rect-2)
	glEnd()
	glDisable(GL_BLEND)
	glEndList()

	liste_line_bas = glGenLists(1)
	glNewList(liste_line_bas, GL_COMPILE)
	glEnable(GL_BLEND)
	glBegin(GL_LINES)
	glVertex2f(x_rect+w_rect, y_rect-1)
	glVertex2f(K.w-(x_rect+w_rect), y_rect-1)
	glEnd()
	glDisable(GL_BLEND)
	glEndList()

	liste_line_gauche = glGenLists(1)
	glNewList(liste_line_gauche, GL_COMPILE)
	glEnable(GL_BLEND)
	glBegin(GL_LINES)
	glVertex2f(K.w-x_rect, y_rect+h_rect)
	glVertex2f(K.w-x_rect, K.h-(y_rect+h_rect))
	glEnd()
	glDisable(GL_BLEND)
	glEndList()

	liste_line_droite = glGenLists(1)
	glNewList(liste_line_droite, GL_COMPILE)
	glEnable(GL_BLEND)
	glBegin(GL_LINES)
	glVertex2f(x_rect, y_rect+h_rect)
	glVertex2f(x_rect, K.h-(y_rect+h_rect))
	glEnd()
	glDisable(GL_BLEND)
	glEndList()
	test_aff = aff_text(K.w2 - w_rect / 2, 0, w_rect, h_rect, "test", pygame.Color(255, 0, 0))
	import tir
	reload(tir)
	tir = tir

	def __init__(__, x=0, y=0, v=0, accel=0.01, vie_max=5):
		__.mousex = K.w2
		__.mousey = K.h2
		#__.relx = K.w2
		#__.rely = K.h2
		__.x = __.x2 = x
		__.y = __.y2 = y
		__.angle = 0
		__.r = 2
		__.vL = 5 * K.temps_boucle / 100.
		__.v = v
		__.vm = __.v
		__.v10 = __.v / 10
		__.vadd = accel * K.temps_boucle / 100.
		__.vmax = 0
		__.score = 0
		__.vie_max = vie_max
		__.vie = __.vie_max
		__.accelere = False
		__.distance = 0
		__.distm = 0
		__.draw_line_cursor = False
		__.d_x = 0
		__.angle_grav = 0
		__.time_accel_pressed = 0
		pygame.mouse.set_visible(False)
	
	def calc_bonus_score(__):
		return (__.v10 /10 + (__.accelere + __.time_accel_pressed * 10) * 10)

	def draw(__):
		if pygame.mouse.get_focused(): pygame.mouse.set_pos(K.w2, K.h2)
		vL = __.vL * (1 + bool(not K.no_grav))

		__.v10 = __.v / 10
		__.dist_mapH = K.largeur_mapH2 - 4
		__.dist_mapV = K.largeur_mapV2 - 4
		__.dist_map = DISTANCE(0, 0, __.dist_mapH, __.dist_mapV)

		if K.mode_cylindre:
			#calcul de l'angle de rotation de la camera
			if not K.no_grav: temp = 90 * K.grav_dir
			else: temp = 0
			if __.angle_grav != temp:
				distance_plus = (temp + 360 - __.angle_grav) % 360
				distance_moins = (__.angle_grav + 360 - temp) % 360
				if distance_plus < distance_moins:
					if (__.angle_grav - temp) % 360 > 1: __.angle_grav += 1
					else: __.angle_grav = temp
				else:
					if (__.angle_grav - temp) % 360 > 1: __.angle_grav -= 1
					else: __.angle_grav = temp

			#calcul des coordonnees
			cos, sin = CoSinus(DIRECTION(0, 0, __.x2, __.y2))
			if not K.no_grav and not (1 != K.grav_dir != 3): cos, sin = sin, cos
			tempx =  - cos * vL
			if abs(tempx) < 5e-2 or abs(tempx) == 2: tempx = __.x2 = 0
			__.angle = (__.angle + tempx) % 360
			if not K.no_grav and not (1 != K.grav_dir != 3): __.mousey -= int(tempx * 10)
			else: __.mousex += int(tempx * 10)
			if K.no_grav:
				tempy = sin * vL
				if abs(tempy) == 2: tempy = __.y2 = 0
				tempy = __.r + tempy

				if 2 <= tempy < __.dist_mapH: __.r = tempy
				elif tempy >= __.dist_mapH: __.r = __.dist_mapH
				elif 2 > tempy: __.r = 2
			else:
				if __.r  + K.grav < __.dist_mapH - 0.1: __.r  += K.grav
				elif __.r >= __.dist_mapH: __.r = __.dist_mapH - 0.1
				if not K.no_grav and not (1 != K.grav_dir != 3): __.x2 = 0
				else: __.y2=0
			Cos, Sin = CoSinus(__.angle + __.angle_grav)
			__.x = Cos * __.r
			__.y = -Sin * __.r

		else:
			cos, sin = CoSinus(DIRECTION(__.x, __.y, __.x2, __.y2))
			if DISTANCE(__.x, __.y, __.x2, __.y2) > vL:
				tempx = __.x + cos * vL
				tempy = __.y - sin * vL
			else:
				tempx = __.x2
				tempy = __.y2
			if K.no_grav or 1 != K.grav_dir != 3:
				if -__.dist_mapH <= tempx <= __.dist_mapH: __.x = tempx
				elif -__.dist_mapH > tempx: __.x = -__.dist_mapH
				elif __.dist_mapH < tempx: __.x = __.dist_mapH
			if K.no_grav or 0 != K.grav_dir != 2:
				if -__.dist_mapV <= tempy <= __.dist_mapV: __.y = tempy
				elif -__.dist_mapV > tempy: __.y = -__.dist_mapV
				elif __.dist_mapV < tempy: __.y = __.dist_mapV

			if not K.no_grav:
				if K.grav_dir ==0:
					__.y2 = __.y
					if __.y - K.grav > -__.dist_mapV: __.y -= K.grav
					else: __.y = -__.dist_mapV
				elif K.grav_dir == 1:
					__.x2 = __.x
					if __.x + K.grav < __.dist_mapH: __.x += K.grav
					else: __.x = __.dist_mapH
				elif K.grav_dir == 2:
					__.y2 = __.y
					if __.y + K.grav < __.dist_mapV: __.y += K.grav
					else: __.y = __.dist_mapV
				elif K.grav_dir == 3:
					__.x2 = __.x
					if __.x - K.grav > -__.dist_mapH: __.x -= K.grav
					else: __.x = -__.dist_mapH

		if __.vie > 0:
			if __.vie > __.vie_max: __.vie = __.vie_max
			if not K.end:
				if __.v < 180:
					__.v += __.vadd
					if __.accelere:
						__.v += __.vadd * 10 + __.time_accel_pressed
						__.time_accel_pressed += 0.00002
						if not __.channel_avance.get_busy(): __.channel_avance.play(__.son_avance)
				else: __.v = 180
				if K.mode_jeu !=2:
					if K.mode_cylindre:
						if K.no_grav: __.score += (__.dist_mapH - 2 - DISTANCE(0, 0, __.x, __.y)) * __.calc_bonus_score()
						else: __.score += 10 * __.calc_bonus_score()
					else:
						if K.no_grav: __.score += (__.dist_map - DISTANCE(0, 0, __.x, __.y)) * __.calc_bonus_score()
						else: __.score += (__.dist_mapH - DISTANCE(0, 0, __.x, 0)) * __.calc_bonus_score()
			elif __.v > 0:
				__.v -= 1
				if __.v < 0: __.v = 0
		else: __.v = 0
		if __.vmax < __.v: __.vmax = __.v
		__.distance += __.v
		if 1000 * __.distm <= __.distance:
			__.vm = __.vm * __.distm + __.v
			__.distm += 1
			__.vm = __.vm / __.distm
		glDeleteTextures(__.tex_vit)
		if __.vie > 0:
			__.tex_vit = surface_to_texture(__.font.render(str(int(__.v/K.temps_boucle*3600)), True, pygame.Color(255, 0, 0)))
		else:
			__.tex_vit = surface_to_texture(__.font.render(str(int(__.vmax/K.temps_boucle*3600)), True, pygame.Color(255, 0, 0)))
		glDeleteTextures(__.tex_dis)
		__.tex_dis = surface_to_texture(__.font.render(str(int(__.distance/1000)), True, pygame.Color(255, 0, 0)))
		glDeleteTextures(__.tex_sco)
		__.tex_sco = surface_to_texture(__.font.render(str(int(__.score)), True, pygame.Color(255, 0, 0)))
		glDeleteTextures(__.tex_deg)
		__.tex_deg = surface_to_texture(__.font.render("["+"="*__.vie + " "*(__.vie_max-__.vie)+"] ", True,
																			pygame.Color(255, 0, 0)))

		#dessine l'interface 2D
		activ_2D(K.w, K.h)
		glColor4ub(255, 0, 0, 200)
		glPointSize(3)
		glPushMatrix()
		if K.mode_cylindre: glTranslatef(K.w2-__.x2, K.h2+__.y2, 0)
		else: glTranslatef(K.w2-__.x2+__.x, K.h2+__.y2-__.y, 0)
		glCallList(__.liste_point)
		glPopMatrix()

		glColor4ub(255, 0, 0, 128)
		glLineWidth(1)
		glCallList(__.liste_cokpit)


		if not K.no_grav and K.grav_dir == 0: alpha = 255; glLineWidth(3)
		else: alpha = 128; glLineWidth(1)
		glColor4ub(255, 0, 0, alpha)
		glCallList(__.liste_line_bas)

		if not K.no_grav and K.grav_dir == 1: alpha = 255; glLineWidth(5)
		else: alpha = 128; glLineWidth(1)
		glColor4ub(255, 0, 0, alpha)
		glCallList(__.liste_line_droite)

		if not K.no_grav and K.grav_dir == 2: alpha = 255; glLineWidth(5)
		else: alpha = 128; glLineWidth(1)
		glColor4ub(255, 0, 0, alpha)
		glCallList(__.liste_line_haut)

		if not K.no_grav and K.grav_dir == 3: alpha = 255; glLineWidth(5)
		else: alpha = 128; glLineWidth(1)
		glColor4ub(255, 0, 0, alpha)
		glCallList(__.liste_line_gauche)
		glCallList(__.test_aff[0])

		if __.draw_line_cursor:
			glLineWidth(1)
			glColor4ub(255, 0, 0, 255)
			glBegin(GL_LINES)
			if K.mode_cylindre:
				glVertex2f(K.w2, K.h2)
				glVertex2f(K.w2-__.x2, K.h2+__.y2)
			else:
				glVertex2f(K.w2, K.h2)
				glVertex2f(K.w2-__.x2+__.x, K.h2+__.y2-__.y)
			glEnd()

		desactiv_2D()

		if K.mode_cylindre:
			__.x2 = __.mousex / K.w2 * __.dist_mapH
			__.y2 = __.mousey / K.h2 * __.dist_mapV + __.r
		else:
			__.x2 = __.mousex / K.w2 * __.dist_mapH
			__.y2 = __.mousey / K.h2 * __.dist_mapV

		#positionne la camera
		if K.mode_cylindre: glRotatef(90 - __.angle, 0, 0, 1)
		gluLookAt(__.x, __.y, 0, __.x, __.y, 10, 0, 1, 0)


	def event(__, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				__.accelere = True
				if not __.vie:
					__.son_panne.play()
				else:
					__.channel_avance.play(__.son_avance)
					__.son_accelere.play()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				__.accelere = False
				__.time_accel_pressed = 0
				__.channel_avance.stop()
		elif event.type == pygame.MOUSEMOTION:
			x, y = event.pos
			__.mousex -= x - K.w2
			__.mousey -= y - K.h2
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 3: __.draw_line_cursor = True
			elif event.button == 1 and K.mode_jeu:
				if K.mode_cylindre:
					cos, sin = CoSinus(__.angle - 90)
					__.tir.Tir((__.x-cos*2, __.y+sin*2, 0), 4)
					__.tir.Tir((__.x+cos*2, __.y-sin*2, 0), 4)
				else:
					__.tir.Tir((__.x-2, __.y, 0), 4)
					__.tir.Tir((__.x+2, __.y, 0), 4)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 3: __.draw_line_cursor = False

