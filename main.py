
import pygame
from CONSTs import *
from forms import FORM
from units import Unit,XY2,Block,Hero,Circle
import camera
display=pygame.display.set_mode(SCREENRECT.size); #Surface

background = pygame.Surface(SCREENRECT.size)
background.fill((0,255,0))
display.blit(background, (0,0))
pygame.display.flip()
	
clock = pygame.time.Clock()
# all = pygame.sprite.RenderUpdates()#RenderUpdates
all = pygame.sprite.Group()
blocks = pygame.sprite.Group()
Unit.containers = all
Block.containers = all,blocks
# Hero.containers = all
Circle.containers=[]
camera = camera.Camera(camera.camera_configure, 10000, 10000) 
# unit=Unit()
Block.initAll()
hero=Hero();
right=False
left=False
up=False
down=False



while RUN_ALL:
	for e in pygame.event.get():
		if e.type == pygame.QUIT or ( e.type==pygame.KEYDOWN and e.key==pygame.K_q):
			RUN_ALL = False
		elif e.type  == pygame.MOUSEBUTTONDOWN:
			if e.button==1:
				pass
				hero.weaponAnim()
				# unit.move(e.pos[0],e.pos[1])
			if e.button==3:
				c=camera.state.topleft
				Circle(e.pos[0]-c[0]-Circle.CircleWidth/2,e.pos[1]-c[1]-Circle.CircleHeight/2)
		elif e.type==pygame.KEYDOWN:
			if e.key==pygame.K_UP:
				up=True
			elif e.key==pygame.K_DOWN:
				down=True
			elif e.key==pygame.K_RIGHT:
				right=True
			elif e.key==pygame.K_LEFT:
				left=True
			elif e.key==pygame.K_SPACE:
				hero.jump_flag=True
				hero.onGround=False
		elif e.type==pygame.KEYUP:
			if e.key==pygame.K_UP:
				up=False
			elif e.key==pygame.K_DOWN:
				down=False
			elif e.key==pygame.K_RIGHT:
				right=False
			elif e.key==pygame.K_LEFT:
				left=False					

	


	
	
	
	
	
	# clear/erase the last drawn sprites
	display.blit(background, (0,0))
	# update all the sprites
	all.update()	#RenderUpdates
	
	hero.update(left, right, up, down, blocks)  # передвижение
	camera.update(hero)
	
	for e in all:
		# display.blit(e.image,[0,0])
		# display.blit(e.image,e.rect)
		display.blit(e.image,camera.apply(e))
		
	display.blit(hero.image,camera.apply(hero))
	
	if hero.weapon.visible:
		x0=hero.rect.x+hero.rect.width/2
		y0=hero.rect.y-hero.rect.width/2
		hero.weapon.update(x0,y0,blocks)
		display.blit(hero.weapon.image,camera.apply(hero.weapon))
	
	# dirty = all.draw(display)	#RenderUpdates
	# pygame.display.update(dirty)	#RenderUpdates
	pygame.display.flip()
	clock.tick(FPS)