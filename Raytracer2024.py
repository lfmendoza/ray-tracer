import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture
from math import radians

width = 256
height = 256

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

# Intentar cargar texturas, si no están disponibles, se usarán colores de respaldo
try:
    floor_texture = Texture("textures/wood_floor.bmp")
except:
    floor_texture = None

try:
    wall_texture = Texture("textures/wall_texture.bmp")
except:
    wall_texture = None

try:
    painting_texture = Texture("textures/painting_texture.bmp")
except:
    painting_texture = None

# Definir materiales con colores de respaldo
marble_color = [0.9, 0.9, 0.9]  # Blanco brillante para mármol
wall_color = [0.8, 0.8, 0.8]    # Gris claro para paredes
wood_color = [0.6, 0.3, 0.1]    # Marrón para madera
metal_color = [0.7, 0.7, 0.7]   # Gris para metal
stone_color = [0.5, 0.5, 0.5]   # Gris oscuro para piedra
leaf_color = [0.2, 0.5, 0.2]    # Verde para hojas
glass_color = [0.9, 0.9, 1.0]   # Casi blanco para vidrio

# Materiales
bricks = Material(diffuse=[1.0,0.2,0.2], spec=128, ks=0.25)
grass = Material(diffuse=[0.2,1.0,0.2], spec=64, ks=0.2)
marble = Material(texture=floor_texture, diffuse=marble_color, spec=64, ks=0.5)
mirror = Material(diffuse=marble_color, spec=128, ks=0.9, matType=REFLECTIVE)
glass = Material(diffuse=glass_color, spec=64, ks=0.1, ior=1.5, matType=TRANSPARENT)
wall_material = Material(texture=wall_texture, diffuse=wall_color, spec=32, ks=0.1)
painting_material = Material(texture=painting_texture, diffuse=[1.0, 1.0, 1.0], spec=16, ks=0.2)
wood = Material(diffuse=wood_color, spec=32, ks=0.2)
metal = Material(diffuse=metal_color, spec=64, ks=0.8)
stone = Material(diffuse=stone_color, spec=16, ks=0.1)
leaf_material = Material(diffuse=leaf_color, spec=8, ks=0.1)

# Dimensiones de la galería
room_width = 20
room_height = 10
room_depth = 30

# Crear las paredes, piso y techo de la galería
left_wall = Plane(position=[-room_width / 2, 0, -room_depth / 2], normal=[1, 0, 0], material=wall_material)
right_wall = Plane(position=[room_width / 2, 0, -room_depth / 2], normal=[-1, 0, 0], material=wall_material)
floor = Plane(position=[0, -room_height / 2, -room_depth / 2], normal=[0, 1, 0], material=marble)
ceiling = Plane(position=[0, room_height / 2, -room_depth / 2], normal=[0, -1, 0], material=wall_material)
back_wall = Plane(position=[0, 0, -room_depth], normal=[0, 0, 1], material=wall_material)
front_wall = Plane(position=[0, 0, 0], normal=[0, 0, -1], material=wall_material)

# Agregar los planos a la escena
rt.scene.extend([left_wall, right_wall, floor, ceiling, back_wall])

# Crear las figuras y colocarlas en la escena

# Triángulo (como pintura en la pared izquierda)
triangle = Triangle(
    v0=[-room_width / 2 + 0.01, 0, -room_depth / 2 + 5],
    v1=[-room_width / 2 + 0.01, 2, -room_depth / 2 + 7],
    v2=[-room_width / 2 + 0.01, -2, -room_depth / 2 + 7],
    material=painting_material
)
rt.scene.append(triangle)

# Pirámide (en el centro de la habitación)
pyramid = Pyramid(
    base_center=[0, -room_height / 2 + 0.01, -room_depth / 2],
    base_size=4,
    height=6,
    material=glass
)
rt.scene.append(pyramid)

# Cono (en el lado derecho de la habitación)
cone = Cone(
    position=[5, -room_height / 2 + 0.01, -room_depth / 2 + 10],
    radius=2,
    height=5,
    material=mirror
)
rt.scene.append(cone)

# OBB (cubo rotado)
obb = OBB(
    position=[-5, -room_height / 2 + 1, -room_depth / 2 + 10],
    sizes=[2, 2, 2],
    rotation=[0, radians(45), 0],
    material=metal
)
rt.scene.append(obb)

# Cilindro (en el fondo de la habitación)
cylinder = Cylinder(
    position=[0, -room_height / 2 + 0.01, -room_depth + 5],
    radius=1.5,
    height=5,
    material=stone
)
rt.scene.append(cylinder)

# Elipsoide (entre el cono y la pirámide)
ellipsoid = Ellipsoid(
    position=[2, -room_height / 2 + 2, -room_depth / 2 + 5],
    radii=[1, 2, 1],
    material=mirror
)
rt.scene.append(ellipsoid)

# Pinturas adicionales en las paredes (usando discos)
painting1 = Disc(
    position=[-room_width / 2 + 0.01, 0, -room_depth / 2 + 15],
    normal=[1, 0, 0],
    radio=2,
    material=painting_material
)
rt.scene.append(painting1)

painting2 = Disc(
    position=[room_width / 2 - 0.01, 0, -room_depth / 2 + 15],
    normal=[-1, 0, 0],
    radio=2,
    material=painting_material
)
rt.scene.append(painting2)

# Agregar plantas (usando conos y esferas)
# Planta 1
trunk1 = Cylinder(
    position=[-3, -room_height / 2 + 0.01, -room_depth / 2 + 8],
    radius=0.2,
    height=2,
    material=wood
)
rt.scene.append(trunk1)

foliage1 = Sphere(
    position=[-3, -room_height / 2 + 2.5, -room_depth / 2 + 8],
    radius=1,
    material=leaf_material
)
rt.scene.append(foliage1)

# Planta 2
trunk2 = Cylinder(
    position=[3, -room_height / 2 + 0.01, -room_depth / 2 + 8],
    radius=0.2,
    height=2,
    material=wood
)
rt.scene.append(trunk2)

foliage2 = Sphere(
    position=[3, -room_height / 2 + 2.5, -room_depth / 2 + 8],
    radius=1,
    material=leaf_material
)
rt.scene.append(foliage2)

# Muebles (usando AABB y OBB)
# Mesa
table_top = AABB(
    position=[0, -room_height / 2 + 1, -room_depth / 2 + 12],
    sizes=[4, 0.2, 2],
    material=wood
)
rt.scene.append(table_top)

# Patas de la mesa
table_legs_positions = [
    [-1.9, -room_height / 2 + 0.5, -room_depth / 2 + 11.9],
    [1.9, -room_height / 2 + 0.5, -room_depth / 2 + 11.9],
    [-1.9, -room_height / 2 + 0.5, -room_depth / 2 + 12.1],
    [1.9, -room_height / 2 + 0.5, -room_depth / 2 + 12.1],
]

for pos in table_legs_positions:
    leg = AABB(
        position=pos,
        sizes=[0.2, 1, 0.2],
        material=wood
    )
    rt.scene.append(leg)

# Lámparas (usando cilindros y esferas)
# Lámpara de techo
lamp_body = Cylinder(
    position=[0, room_height / 2 - 1, -room_depth / 2 + 5],
    radius=0.5,
    height=2,
    material=metal
)
rt.scene.append(lamp_body)

lamp_light = Sphere(
    position=[0, room_height / 2 - 2.5, -room_depth / 2 + 5],
    radius=0.5,
    material=glass
)
rt.scene.append(lamp_light)

# Agregar luces para las lámparas
rt.lights.append(PointLight(position=[0, room_height / 2 - 2.5, -room_depth / 2 + 5], intensity=1.5, color=[1.0, 0.9, 0.8]))

# Agregar luces para resaltar las pinturas
rt.lights.append(AmbientLight(intensity=0.2))
rt.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity=0.2))
rt.lights.append(SpotLight(position=[-room_width / 2 + 1, 2, -room_depth / 2 + 6], direction=[1, -0.5, 0], intensity=2, innerAngle=20, outerAngle=30))
rt.lights.append(SpotLight(position=[room_width / 2 - 1, 2, -room_depth / 2 + 6], direction=[-1, -0.5, 0], intensity=2, innerAngle=20, outerAngle=30))

# Agregar luces de diferentes tonos e intensidades
rt.lights.append(PointLight(position=[0, room_height / 2 - 0.5, -room_depth / 2], intensity=1.0, color=[1.0, 0.95, 0.8]))  # Luz cálida
rt.lights.append(PointLight(position=[0, -room_height / 2 + 0.5, -room_depth / 2], intensity=0.5, color=[0.8, 0.9, 1.0]))  # Luz fría

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