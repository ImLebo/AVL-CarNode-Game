import pygame
from pygame.locals import *


class End:
	def __init__(self, screen, width, height, fondo=None):
		self.screen = screen
		self.width = width
		self.height = height
		self.fondo = fondo
		self.font = pygame.font.SysFont('Arial', 48)
		self.text = self.font.render('¡Meta!', True, (255, 255, 255))
		self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2 - 50))
		self.subtext = self.font.render('¡Felicidades, llegaste a la meta!', True, (255, 215, 0))
		self.subtext_rect = self.subtext.get_rect(center=(self.width // 2, self.height // 2 + 30))

	def iniciar(self):
		pass

	def manejar_eventos(self, eventos):
		for event in eventos:
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				# Aquí podrías regresar al menú principal si lo deseas
				pass

	def actualizar(self):
		pass

	def dibujar(self, pantalla):
		if self.fondo:
			pantalla.blit(self.fondo, (0, 0))
		else:
			pantalla.fill((135, 206, 250))
		pantalla.blit(self.text, self.text_rect)
		pantalla.blit(self.subtext, self.subtext_rect)
