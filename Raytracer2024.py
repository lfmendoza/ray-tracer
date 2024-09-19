import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import Material
from lights import *

width = 512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)

bricks = Material(diffuse=[1.0,0.2,0.2], spec=128, ks=0.25)
grass = Material(diffuse=[0.2,1.0,0.2], spec=64, ks=0.2)
button = Material(diffuse=[0.1,0,0], spec=114, ks=0.4)
snow = Material(diffuse=[0.4,0.4,0.5], spec=364, ks=0.66)
carrot = Material(diffuse=[2,0.9,0.3], spec=91, ks=0.71)

rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intesity=0.8))
rt.lights.append(DirectionalLight(direction=[0.5,-0.5,-1], intesity=0.8, color=[1,1,1]))
rt.lights.append(DirectionalLight(direction=[16,1,2], intesity=0.9, color=[0,1,1]))
rt.lights.append(AmbientLight(intesity=0.4))

# smile
rt.scene.append(Sphere(position=[-0.4, 1.58, -9], radius=0.05, material=button))
rt.scene.append(Sphere(position=[0.3, 1.58, -9], radius=0.05, material=button))
rt.scene.append(Sphere(position=[-0.15, 1.5, -9], radius=0.05, material=button))
rt.scene.append(Sphere(position=[0.15, 1.5, -9], radius=0.05, material=button))

# eyes
rt.scene.append(Sphere(position=[0.25, 2.45, -9], radius=0.1, material=button))
rt.scene.append(Sphere(position=[-0.25, 2.45, -9], radius=0.1, material=button))

# noise
rt.scene.append(Sphere(position=[0, 1.9, -9], radius=0.25, material=carrot))

# buttons
rt.scene.append(Sphere(position=[0, 1, -9], radius=0.2, material=button))
rt.scene.append(Sphere(position=[0, -0.4, -9], radius=0.2, material=button))
rt.scene.append(Sphere(position=[0, -1.7, -9], radius=0.5, material=button))

# Snowman
rt.scene.append(Sphere(position=[0, 2.2, -10], radius=0.95, material=snow))
rt.scene.append(Sphere(position=[0, 0.3, -10], radius=1.2, material=snow))
rt.scene.append(Sphere(position=[0, -2, -10], radius=1.5, material=snow))

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
	
pygame.quit()