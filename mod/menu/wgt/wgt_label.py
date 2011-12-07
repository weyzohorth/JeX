import pygame

class Wgt_label:
	events = []

	def __init__(__, boss, x, y, w=100, h=20, text="", coul=(0, 0, 0), coul_font=(255, 255, 255), font="data/fonts/comic.ttf"):
		__.boss = boss
		__.x, __.y = x, y
		__.w, __.h = w, h
		__.text = text
		__.font = pygame.font.Font(font, int(__.h / 2))
		__.surface = pygame.Surface((__.w, __.h))
		__.coul_font = coul_font
		__.coul = coul

	def blit(__):
		__.surface.fill(__.coul)
		__.surface.blit(__.font.render(__.text, 1, __.coul_font), (0, 0))
		__.boss.blit(__.surface, (__.x, __.y))
