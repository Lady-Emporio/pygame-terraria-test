import pygame
class FORM(pygame.Surface):
	def __init__(self,size):
		pygame.Surface.__init__(self,size)
		self.isActive=False;
		self.fill((255,0,0))