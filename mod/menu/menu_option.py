from mod.__init__ import *
from random import randrange
from wgt.wgt_progression import *
from wgt.wgt_bouton import *
from wgt.wgt_label import *

class Menu_option(K.menu.__class__):
	def __init__(__, boss):
		__.boss = boss
		__.back = __.boss.back
		__.screen = __.boss.screen
		__.wgt = {"fullscreen":None, "label_musique":None, "label_effets":None,
						"volume_musique":None, "volume_effets":None, "particules":None, "OK":None}
		__.wgt["fullscreen"] = Wgt_bouton(__.boss.screen, 100, 100, 200, text="fullscreen", checkable=True)
		__.wgt["fullscreen"].checked = __.boss.fullscreen
		__.wgt["particules"] = Wgt_bouton(__.boss.screen, 100, 130, 200, text="particules", checkable=True)
		__.wgt["particules"].checked = True
		__.wgt["label_musique"] = Wgt_label(__.boss.screen, 100, 160, text="volume musique")
		__.wgt["volume_musique"] = Wgt_progression(__.boss.screen, 100, 180, 200,
												value=int(pygame.mixer.music.get_volume()*100))
		__.wgt["label_effets"] = Wgt_label(__.boss.screen, 100, 200, text="volume effets")
		__.wgt["volume_effets"] = Wgt_progression(__.boss.screen, 100, 220, 200, value=100)
		def ok(__): __.running = False
		__.wgt["OK"] = Wgt_bouton(__.boss.screen, 100, 240, 200, fonction=lambda:ok(__))
		__.running = True
		__.musiques = __.boss.musiques
		__.lim_musiques = __.boss.lim_musiques
		__.boucle()

	def get_info(__):
		pass
	
	def quit(__):
		__.boss.fullscreen = __.wgt["fullscreen"].checked
		K.particules = __.wgt["particules"].checked
		K.vol_musique = __.wgt["volume_musique"].get()
		K.vol_effet = __.wgt["volume_effets"].get()
		pygame.mixer.music.set_volume(K.vol_musique/100.)
		__.boss.wgt["options"].checked = False
#	def boucle(__):
#		while __.running:
#			for i in __.wgt.values(): i.blit()
#			__.event()
#			pygame.display.update()
#			pygame.time.wait(40)
#
#	def event(__):
#		for i in pygame.event.get():
#			if i.type == pygame.QUIT: __running = False
#			for wgt in __.wgt.values():
#				if i.type in wgt.events: wgt.event(i)
