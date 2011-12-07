# -*- coding: cp1252 -*-
import pygame
pygame.init()

class Global:
	def __init__(__):
		# mode_jeu:
		# 0 - standard arriver à la fin du niveau en évitant obstacle
		# 1 - mode tirer dans une sphere sans mourir avant la fin du niveau
		# 2 - mode space invader tiez dans tous les blocs pour les détruire et les empêcher de continuer
		__.mode_jeu = 0
		__.menu = None
		__.map = "map/random.bex"
		__.version = "0.8.1"
		__.temps_boucle = 40

K = Global()
