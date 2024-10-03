import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture

width = 512
height = 512

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

# Cargar texturas (si están disponibles)
# try:
#     floor_texture = Texture("textures/wood_floor.bmp")
# except:
    # floor_texture = None
floor_texture = None

bricks = Material(diffuse=[1.0,0.2,0.2], spec=128, ks=0.25)
grass = Material(diffuse=[0.2,1.0,0.2], spec=64, ks=0.2)

mirror = Material(diffuse=[0.9,0.9,0.9], spec=128, ks=0.2, matType=REFLECTIVE)
blueMirror = Material(diffuse=[0.5,0.5,0.1], spec=128, ks=0.2, matType=REFLECTIVE)
glass = Material(spec=128, ks=0.2, ior=1.5, matType=TRANSPARENT)
water = Material(spec=56, ks=0.4, ior=1.33, matType=TRANSPARENT)

wall_material = Material(diffuse=[0.9, 0.9, 0.9], spec=32, ks=0.1)  # Paredes gris claro
floor_material = Material(diffuse=[0.8, 0.7, 0.6], spec=16, ks=0.3)  # Piso marrón claro
if floor_texture:
    floor_material.texture = floor_texture
ceiling_material = Material(diffuse=[0.95, 0.95, 0.95], spec=8, ks=0.05)  # Techo blanco
back_wall_material = Material(diffuse=[0.9, 0.9, 0.9], spec=32, ks=0.1)  # Pared de fondo

# Otros materiales
# marble = Material(texture=Texture("textures/marble.bmp"), spec=128, ks=0.2)
# carton = Material(texture=Texture("textures/carton.bmp"), spec=8, ks=0.2)
bricks = Material(diffuse=[0.8, 0.3, 0.3], spec=128, ks=0.25)

# Dimensiones del cuarto
room_width = 25
room_height = 15
room_depth = 30

# Crear las paredes del cuarto usando planos
left_wall = Plane(position=[-room_width / 2, 0, -room_depth / 2], normal=[1, 0, 0], material=wall_material)
right_wall = Plane(position=[room_width / 2, 0, -room_depth / 2], normal=[-1, 0, 0], material=wall_material)
floor = Plane(position=[0, -room_height / 2, -room_depth / 2], normal=[0, 1, 0], material=floor_material)
ceiling = Plane(position=[0, room_height / 2, -room_depth / 2], normal=[0, -1, 0], material=mirror)
back_wall = Plane(position=[0, 0, -room_depth], normal=[0, 0, 1], material=back_wall_material)

# Agregar los planos a la escena
rt.scene.extend([left_wall, right_wall, floor, ceiling, back_wall])

# Crear dos cubos (AABB) en las esquinas del piso
cube_size = 2
cube_positions = [
    [-room_width / 2 + cube_size / 2 + 0.1, -room_height / 2 + cube_size / 2, -room_depth + cube_size / 2 + 0.1],  # Esquina izquierda trasera
    [room_width / 2 - cube_size / 2 - 0.1, -room_height / 2 + cube_size / 2, -room_depth + cube_size / 2 + 0.1],   # Esquina derecha trasera
]

cube_materials = [grass, blueMirror]
for pos, mat in zip(cube_positions, cube_materials):
    cube = AABB(position=pos, sizes=[cube_size, cube_size, cube_size], material=mat)
    rt.scene.append(cube)

# Crear un disco en el centro del piso apuntando hacia el techo
disc = Disc(position=[0, -room_height / 2 + 0.01, -room_depth / 2], normal=[0, 1, 0], radio=3, material=bricks)
rt.scene.append(disc)

# Material de las lámparas (transparente para no bloquear la luz)
lamp_material = Material(diffuse=[1.0, 1.0, 1.0], spec=0, ks=0.0, matType=TRANSPARENT, ior=1.0)

lamp_size = [4, 0.1, 2]  # Dimensiones de la lámpara

# Posiciones de las lámparas
lamp_positions = [
    [-room_width / 4, room_height / 2 - lamp_size[1] / 2 - 0.1, -room_depth / 4],
    [room_width / 4, room_height / 2 - lamp_size[1] / 2 - 0.1, -room_depth / 4],
    [-room_width / 4, room_height / 2 - lamp_size[1] / 2 - 0.1, -3 * room_depth / 4],
    [room_width / 4, room_height / 2 - lamp_size[1] / 2 - 0.1, -3 * room_depth / 4],
    [0, room_height / 2 - lamp_size[1] / 2 - 0.1, -room_depth / 2],
    [0, room_height / 2 - lamp_size[1] / 2 - 0.1, -room_depth + lamp_size[2]],
]

# Lámparas como AABB transparentes y agregarlas a la escena
for pos in lamp_positions:
    lamp = AABB(position=pos, sizes=lamp_size, material=lamp_material)
    rt.scene.append(lamp)

# Agregar luces
rt.lights.append(AmbientLight(intensity=0.2))
rt.lights.append(DirectionalLight(direction=[0, -1, 0], intensity=0.2))

# SpotLights en las posiciones de las lámparas
for pos in lamp_positions:
    rt.lights.append(SpotLight(position=pos, direction=[0, -1, 0], intensity=5, innerAngle=50, outerAngle=70))

# Luz puntual en el centro del techo
rt.lights.append(PointLight(position=[0, room_height / 2 - 0.5, -room_depth / 2], intensity=1.0))

# Renderizar la escena
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
