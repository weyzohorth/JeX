from mod.fct.mod_gl import *
from random import randrange
from mod.fct.mod_file import get_allfiles
from mod.fct.save import save_highscore
from os import remove

class Game:
	def __init__(__, w=960, h=720, fullscreen=0, resolution_screen=()):
		K.n, K.f = 1, 300
		K.Game = __
		pygame.display.init()
		if fullscreen:
			if not resolution_screen:
				Info = pygame.display.Info()
				K.w, K.h = Info.current_w, Info.current_h
			else: K.w, K.h = resolution_screen
		else: K.w, K.h = w, h
		init(K.w, K.h, K.n, K.f, 150, pygame.RESIZABLE | pygame.FULLSCREEN*fullscreen)
		pygame.display.set_caption("jeX","jeX : go ultra fast")

		K.w2, K.h2 = K.w/2., K.h/2.

		glBlendFunc(GL_SRC_ALPHA,GL_ONE)
		__.musiques = list(get_allfiles("data/sounds/music/jeu"))
		__.lim_musiques = len(__.musiques)
		__.boucle()

	def init_obj(__):
		import map
		reload(map)
		__.map = map.Map(__, 50, 50, 800, filename=K.map)
		import joueur
		reload(joueur)
		K.joueur = joueur.Joueur(vie_max=5)

	def draw(__):
		K.joueur.draw()
		__.map.draw()

	def event(__):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: __.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: __.running = False
			if event.type in K.joueur.event_types: K.joueur.event(event)


	def boucle(__):
		__.init_obj()
		__.temps = pygame.time.get_ticks()
		__.running = True
		while __.running:
			if not pygame.mixer.music.get_busy() and K.joueur.vie:
				pygame.mixer.music.load(__.musiques[randrange(__.lim_musiques)])
				pygame.mixer.music.play()
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			gluPerspective(70+K.joueur.v/2, 1, K.n, K.f)
			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()
			__.draw()
			__.event()
			pygame.display.flip()
			temp = pygame.time.get_ticks()
			temps_passe = temp  - __.temps
			__.temps = temp
			pygame.time.wait(K.temps_boucle - temps_passe)
		save_highscore(K.joueur, K.mode_jeu, K.map)
		__.map.Interp.fichier.close()
		K.obj = []
		glDeleteLists(1, 13)
		glDeleteTextures(K.joueur.tex_vit)
		glDeleteTextures(K.joueur.tex_vitesse)
		glDeleteTextures(K.joueur.tex_dis)
		glDeleteTextures(K.joueur.tex_distance)
		glDeleteTextures(K.joueur.tex_sco)
		glDeleteTextures(K.joueur.tex_score)
		glDeleteTextures(K.joueur.tex_deg)
		glDeleteTextures(K.joueur.tex_degat)
		if not K.menu: pygame.quit()
		if __.map.Interp.filename: remove(__.map.Interp.filename)
