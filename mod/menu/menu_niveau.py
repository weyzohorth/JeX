from mod.fct.mod_gl import *
from mod.fct.mod_file import *
from mod.fct.save import *
from mod.obj.game import Game
from wgt.wgt_bouton import *
from wgt.wgt_liste import *
from wgt.wgt_progression import *
from wgt.wgt_label import *
from random import randrange

class Menu_niveau:
	text_list = ("score : ", "distance : ", "vitesse maximale : ", "vitesse moyenne : ", "vie : ")
	def __init__(__):
		def fonction(__):
			K.map = "map/" + __.wgt["map"].get()
			K.mode_jeu = __.wgt["mode"].get_index()
			pygame.mixer.music.fadeout(3000)
			if __.fullscreen:
				try: Game(fullscreen=__.fullscreen, resolution_screen=(__.screen_w, __.screen_h))
				except Exception, err: print err
			else: Game(fullscreen=__.fullscreen)
			pygame.mixer.music.fadeout(1000)
			__.screen = pygame.display.set_mode((640, 480))
			__.wgt["options"].checked = False
			pygame.mouse.set_visible(True)
			__.oldmap = ""
		#######################################################
		if not pygame.display.get_init(): pygame.display.init()
		Info = pygame.display.Info()
		__.screen_w, __.screen_h = Info.current_w, Info.current_h
		__.musiques = list(get_allfiles("data/sounds/music/menu"))
		__.lim_musiques = len(__.musiques)
		pygame.mixer.music.load(__.musiques[randrange(__.lim_musiques)])
		pygame.mixer.music.play()
		K.menu = __
		__.w, __.h = 640, 480
		__.oldmap = ""
		__.screen = pygame.display.set_mode((__.w, __.h))
		__.back = pygame.Surface((__.w, __.h))
		__.fullscreen = False
		__.wgt = {"map":None, "mode":None, "jouer":None, "options":None, "scores_list":None,
						"score":None, "distance":None, "vmax":None, "vm":None, "vie":None}
		__.wgt["map"] = Wgt_liste(__.screen, 320, 0, 320, 460, 15)
		for i in get_files("map"):
			ext = get_ext(i)
			if ext == "jex" or ext == "bex": __.wgt["map"].add_item(i)
		__.wgt["mode"] = Wgt_liste(__.screen, 100, 120, 220, 60, 3)
		__.wgt["mode"].add_item("mode normal")
		__.wgt["mode"].add_item("mode detruire toute les spheres")
		__.wgt["mode"].add_item("mode space invaders")
		__.wgt["scores_list"] = Wgt_liste(__.screen, 100, 200, 220, 100, 5)
		__.wgt["scores_list"].add_item("meilleur score")
		__.wgt["scores_list"].add_item("meilleur distance")
		__.wgt["scores_list"].add_item("meilleur vistesse maximale")
		__.wgt["scores_list"].add_item("meilleur vitesse moyenne")
		__.wgt["scores_list"].add_item("meilleur survie")
		coul = (20, 20, 20)
		__.wgt["score"] = Wgt_label(__.screen, 100, 350, w=220, text=__.text_list[0], coul=coul)
		__.wgt["distance"] = Wgt_label(__.screen, 100, 370, w=220, text=__.text_list[1], coul=coul)
		__.wgt["vmax"] = Wgt_label(__.screen, 100, 390, w=220, text=__.text_list[2], coul=coul)
		__.wgt["vm"] = Wgt_label(__.screen, 100, 410, w=220, text=__.text_list[3], coul=coul)
		__.wgt["vie"] = Wgt_label(__.screen, 100, 430, w=220, text=__.text_list[4], coul=coul)
		__.wgt["jouer"] = Wgt_bouton(__.screen, 320, 460, 320, text="Jouer", fonction=lambda: fonction(__))
		import menu_option
		__.wgt["options"] = Wgt_bouton(__.screen, 100, 100, text="options", fonction=lambda: menu_option.Menu_option(__))
		__.running = True
		__.boucle()

	def get_info(__):
		map = get_mappath(__.wgt["map"].get(), __.wgt["mode"].get_index())
		if __.oldmap == map:
			return
		__.oldmap = map
		dic = put_file_in_dict(map)
		key = dic_keys[__.wgt["scores_list"].get_index()]
		for i, key in enumerate(dic_keys):
			if key[0 : 2] == "vm":
				__.wgt[key].text = __.text_list[i] + str(dic[key][i] / float(K.temps_boucle) * 3600)
			elif key[0] == 'd':
				__.wgt[key].text = __.text_list[i] + str(dic[key][i] / 1000)
			else:
				__.wgt[key].text = __.text_list[i] + str(dic[key][i])
		
	def boucle(__):
		while __.running:
			if not pygame.mixer.music.get_busy():
				pygame.mixer.music.load(__.musiques[randrange(__.lim_musiques)])
				pygame.mixer.music.play()
			__.screen.blit(__.back, (0, 0))
			for wgt in __.wgt.values(): wgt.blit()
			__.event()
			__.get_info()
			pygame.display.update()
			pygame.time.wait(100)
		__.quit()

	def quit(__):
		pygame.quit()

	def event(__):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: __.running = False
			for wgt in __.wgt.values():
				if event.type in wgt.events: wgt.event(event)

if __name__ == "__main__":
	Menu_niveau()
