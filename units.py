import numpy as np
from scipy.ndimage.interpolation import zoom

import pygame
import math
from CONSTs import *
class Unit(pygame.sprite.Sprite):
	speed = 0.06
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.image = pygame.Surface([20, 20])
		self.image.fill( (0,0,255) )
		self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
		
		
		self.moveTo=[0,0]
		self.stop=True
		self.stepx=0;
		self.stepy=0;
		
		self.Xgo=self.rect.x;
		self.Ygo=self.rect.y;
	def update(self):
		if(self.stepx!=0):
			self.Xgo+=self.stepx;	
		if(self.stepy!=0):
			self.Ygo+=self.stepy;
		
		if self.stepx>0:
			if self.Xgo>=self.moveTo[0]:
				self.Xgo=self.moveTo[0]
				self.stepx=0;
		elif self.stepx<0:
			if self.Xgo<=self.moveTo[0]:
				self.Xgo=self.moveTo[0]
				self.stepx=0;
		
		if self.stepy>0 :
			if(self.Ygo>=self.moveTo[1]):
				self.Ygo=self.moveTo[1]
				self.stepy=0
		elif self.stepy<=0:
			if(self.Ygo<=self.moveTo[1]):
				self.Ygo=self.moveTo[1]
				self.stepy=0
	
		self.rect.x=self.Xgo;
		self.rect.y=self.Ygo;
		

		
		
		
		
		
		
		
		
		
		
		

	def move(self,x,y):
		self.moveTo[0]=x-self.rect.width/2
		self.moveTo[1]=y-self.rect.height/2
		this=pygame.math.Vector2(self.rect.x,self.rect.y)
		needWalk=math.ceil( this.distance_to( pygame.math.Vector2(self.moveTo[0],self.moveTo[1]) ) )
		if(needWalk==0):
			return
		time=float(needWalk/self.speed)

		dx, dy = (self.rect.x - self.moveTo[0], self.rect.y - self.moveTo[1])
		# self.stepx, self.stepy = (-dx / 30., -dy / 30.)
		self.stepx, self.stepy = (-dx / (time/FPS), -dy / (time/FPS) )
	
class XY2(Unit):
	limitX=8
	def __init__(self,createX,createY,down=True,right=True,color=(169, 169, 169)):
		Unit.__init__(self)
		self.image.fill( color )
		self.limit=0;
		self.createX=createX
		self.createY=createY
		self.rect.x=self.createX
		self.rect.y=self.createY
		self.down=down	#boolean
		self.right=right	#boolean

	def update(self):
		if (self.limit>=self.limitX and self.right) or (
		self.limit<=0 and not self.right):
			# self.limit=0;
			self.right=not self.right
			
		if self.right:
			self.limit+=0.03
		else:
			self.limit-=0.03
		
		result=math.sin(self.limit)*100
		
		if self.down:
			result=-result
		
		self.rect.x=self.createX+self.limit*100;
		self.rect.y=self.createY+result;

	
class Block(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.image = pygame.Surface([20, 20])
		self.image.fill( (255, 20, 147) )
		self.rect = self.image.get_rect()
	def initAll():
		# np.set_printoptions(threshold=1)
		# arr = np.random.uniform(size=(10,5))
		arr = np.random.normal(0, 1, size=(10,5))
		# arr = np.random.vonmises(0, 1, size=(10,5))
		# arr = np.random.wald(0.4,1,size=(10,5))
		arr = zoom(arr, 8)
		row_max=len(arr)
		col_max=len(arr[0])
		for row in range(row_max):
			for col in range(col_max):
				value=arr[row][col]
				block=Block()
				block.rect.x=row*21+5
				block.rect.y=col*21+160
				if value<0.1:
					block.image.fill( (0, 0, 0) ) 
					
					block.kill()
					
				elif value<0.2: 
					block.image.fill( (192, 192, 192) )
				elif value<0.3: 
					block.image.fill( (255, 255, 255) )
				elif value<0.4: 
					block.image.fill( (255, 0, 255) )
				elif value<0.5:
					block.image.fill( (128, 0, 128) )
				elif value<0.6: block.image.fill( (255, 255, 0) )
				elif value<0.7: block.image.fill( (128, 128, 0) )
				elif value<0.8: block.image.fill( (0, 128, 0) )
				elif value<0.9: block.image.fill( (0, 255, 255) )
				elif value<0.10:
					block.image.fill( (0, 0, 128) )

class Circle(Unit):
	radius=60/2
	CircleWidth=20
	CircleHeight=20
	def __init__(self,x,y):
		Unit.__init__(self)
		self.image = pygame.Surface([self.CircleWidth, self.CircleHeight])
		self.image.fill( (0,0,255) )
		self.rect = self.image.get_rect()

		self.x0=x;
		self.y0=y
		self.rect.x=self.x0
		self.rect.y=self.y0
		self.angle=-1.5
		
		self.visible=False
	def update(self):
		x = self.x0 + self.radius * math.cos(self.angle)
		y = self.y0 + self.radius * math.sin(self.angle)
		
		self.angle += 0.1
		if self.angle>1.7:
			self.angle=-1.5
			self.visible=False
		self.rect.x=x
		self.rect.y=y
		print([self.angle,self.rect])
		
	def update(self,x0,y0,blocks):
		x = x0 + self.radius * math.cos(self.angle)
		y = y0 + self.radius * math.sin(self.angle)
		
		self.angle += 0.1
		if self.angle>1.7:
			self.angle=-1.5
			self.visible=False
		self.rect.x=x
		self.rect.y=y
		
		block=pygame.sprite.spritecollideany(self,blocks)
		if block!=None:
			block.kill()
			self.angle=-1.5
			self.visible=False
		
		
			
class Hero(pygame.sprite.Sprite):
	speed=4
	jump_speed=10
	jump_iter=0;
	gravity=3;
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20, 40])
		self.image.fill( (255, 0, 0) )
		self.rect = self.image.get_rect()
		self.rect.x=40;
		self.rect.y=2
		self.jump_height=50;
		self.jump_flag=False
		self.onGround=False
		
		self.weapon=Circle(0,0)
	def moveRight(self):
		self.rect.move_ip(self.speed,0)
	def moveTop(self):
		self.rect.move_ip(0,-self.speed)
	def moveLeft(self):
		self.rect.move_ip(-self.speed,0)
	def moveDown(self):
		self.rect.move_ip(0,self.speed)
		
	def weaponAnim(self):
		self.weapon.visible=True
		self.weapon.x0=self.rect.x+self.rect.width/2
		self.weapon.y0=self.rect.y-self.rect.width/2
		
	def update(self,left, right, up, down, blocks):
		
		
		move_y=0
		
		if self.jump_flag:
			self.jump_iter+=1
			move_y-=self.jump_speed;
			
		if self.jump_iter==7:
			self.jump_flag=False
			self.jump_iter=0
			
		if not self.onGround:
			move_y +=  self.gravity
		self.onGround = False
		self.rect.y+=move_y 
		self.collide(0,move_y, blocks)
		
		move_x=0
		if left:
			move_x = -self.speed # Лево = x- n
		if right:
			move_x= self.speed
		self.rect.x += move_x
		
		
		self.collide(move_x,0, blocks)
		
		


	def collide(self, xvel, yvel, blocks):

		for block in pygame.sprite.spritecollide(self,blocks,False):
			if xvel > 0:			# если движется вправо
				 self.rect.right = block.rect.left
			if xvel < 0:			# если движется влево
				self.rect.left = block.rect.right
			if yvel > 0:	 # если падает вниз
				self.rect.bottom = block.rect.top
			if yvel < 0:# если движется вверх	
				self.rect.top = block.rect.bottom

Notepad=True
	
	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	