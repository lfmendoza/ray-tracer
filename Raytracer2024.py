import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture

width = 256
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/parkingLot.bmp")

bricks = Material(diffuse=[1.0,0.2,0.2], spec=128, ks=0.25)
grass = Material(diffuse=[0.2,1.0,0.2], spec=64, ks=0.2)

mirror = Material(diffuse=[0.9,0.9,0.9], spec=128, ks=0.2, matType=REFLECTIVE)
blueMirror = Material(diffuse=[0.5,0.5,0.1], spec=128, ks=0.2, matType=REFLECTIVE)

# earth = Material(texture=Texture("textures/earthDay.bmp"))
# marble = Material(texture=Texture("textures/whiteMarble.bmp"), spec=128, ks=0.2, matType=REFLECTIVE)
glass = Material(spec=128, ks=0.2, ior=1.5, matType=TRANSPARENT)

rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intesity=0.8))
rt.lights.append(AmbientLight(intesity=0.1))

rt.scene.append(Sphere(position=[0,0,-5], radius=1.5, material=glass))

rt.glRender()

isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
				
	pygame.display.flip()
	clock.tick(60)

rt.glGenerateFrameBuffer('output.bmp')
	
pygame.quit()