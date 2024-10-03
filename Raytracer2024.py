import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture

width = 360
height = 360

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
water = Material(spec=56, ks=0.4, ior=1.33, matType=TRANSPARENT)
# woodenBox = Material(texture="textures/woodenBox.bmp")

# rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intesity=0.8))
rt.lights.append(AmbientLight(intesity=0.1))
rt.lights.append(SpotLight(position=[2,0,-5], direction=[-1,0,0], intensity=2))

# rt.scene.append(Sphere(position=[0,0,-5], radius=1.5, material=glass))
# rt.scene.append(Plane(position=[0, -5,-5], normal=[0,1,0], material=bricks))
# rt.scene.append(Disc(position=[0,-1,-5], normal=[0,1,0], radio=1.5, material=mirror))

# rt.scene.append(AABB(position=[1.5,1.5,-5], sizes=[1,1,1], material=bricks))
# rt.scene.append(AABB(position=[-1.5,1.5,-5], sizes=[1,1,1], material=mirror))
# rt.scene.append(AABB(position=[1.5,-1.5,-5], sizes=[1,1,1], material=grass))
# rt.scene.append(AABB(position=[-1.5,-1.5,-5], sizes=[1,1,1], material=glass))

rt.scene.append(Plane(position=[0, -1, 0], normal=[0,1,0], material=bricks))

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