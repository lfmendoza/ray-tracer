import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture
from math import radians

width = 512
height = 512

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/parkingLot.bmp")

# Definir materiales con colores para emular texturas
mountain_color = [0.5, 0.35, 0.05]  # Marrón para montañas
tree_trunk_color = [0.55, 0.27, 0.07]  # Marrón oscuro para troncos
leaf_color = [0.13, 0.55, 0.13]  # Verde para hojas
water_color = [0.0, 0.5, 0.7]  # Azul para agua
sun_color = [1.0, 0.84, 0.0]  # Amarillo para el sol
rock_color = [0.4, 0.4, 0.4]  # Gris para rocas

# Materiales
mountain_material_opaco = Material(diffuse=mountain_color, spec=16, ks=0.1)
mountain_material_reflective = Material(diffuse=mountain_color, spec=64, ks=0.5, matType=REFLECTIVE)
tree_trunk_material = Material(diffuse=tree_trunk_color, spec=8, ks=0.1)
leaf_material = Material(diffuse=leaf_color, spec=32, ks=0.3, matType=TRANSPARENT, ior=1.3)
water_material = Material(diffuse=water_color, spec=96, ks=0.8, matType=REFLECTIVE)
rock_material = Material(diffuse=rock_color, spec=32, ks=0.2)
sun_material = Material(diffuse=sun_color, spec=128, ks=1.0, matType=EMISSIVE)

# Remover los planos de la habitación
rt.scene = []

# Crear el paisaje

# Montañas (usando conos y pirámides)
# Montaña 1 (cono opaco)
mountain1 = Cone(
    position=[-5, -2, -20],
    radius=5,
    height=10,
    material=mountain_material_opaco
)
rt.scene.append(mountain1)

# Montaña 2 (pirámide reflectiva)
mountain2 = Pyramid(
    base_center=[5, -2, -25],
    base_size=10,
    height=12,
    material=mountain_material_reflective
)
rt.scene.append(mountain2)

# Montaña 3 (cono reflectivo)
mountain3 = Cone(
    position=[0, -2, -30],
    radius=7,
    height=15,
    material=mountain_material_reflective
)
rt.scene.append(mountain3)

# Árboles (usando cilindros y esferas)
# Árbol 1
tree_trunk1 = Cylinder(
    position=[-10, -3, -15],
    radius=0.5,
    height=3,
    material=tree_trunk_material
)
rt.scene.append(tree_trunk1)

tree_leaves1 = Sphere(
    position=[-10, 0.5, -15],
    radius=2,
    material=leaf_material
)
rt.scene.append(tree_leaves1)

# Árbol 2
tree_trunk2 = Cylinder(
    position=[10, -3, -18],
    radius=0.5,
    height=3,
    material=tree_trunk_material
)
rt.scene.append(tree_trunk2)

tree_leaves2 = Sphere(
    position=[10, 0.5, -18],
    radius=2,
    material=leaf_material
)
rt.scene.append(tree_leaves2)

# Árbol 3
tree_trunk3 = Cylinder(
    position=[-7, -3, -22],
    radius=0.5,
    height=4,
    material=tree_trunk_material
)
rt.scene.append(tree_trunk3)

tree_leaves3 = Cone(
    position=[-7, 1, -22],
    radius=2,
    height=3,
    material=leaf_material
)
rt.scene.append(tree_leaves3)

# Lago (usando plano horizontal)
lake = Plane(
    position=[0, -3, -20],
    normal=[0, 1, 0],
    material=water_material
)
rt.scene.append(lake)

# Rocas (usando elipsoides)
# Roca 1
rock1 = Ellipsoid(
    position=[2, -2.8, -17],
    radii=[1, 0.5, 0.5],
    material=rock_material
)
rt.scene.append(rock1)

# Roca 2
rock2 = Ellipsoid(
    position=[-3, -2.9, -19],
    radii=[0.7, 0.3, 0.5],
    material=rock_material
)
rt.scene.append(rock2)

# Sol (usando esfera emisiva)
sun = Sphere(
    position=[0, 10, -50],
    radius=5,
    material=sun_material
)
rt.scene.append(sun)

# Agregar luces
# Luz ambiental cálida para simular el atardecer
rt.lights.append(AmbientLight(intensity=0.3, color=[1.0, 0.7, 0.5]))

# Luz direccional simulando la luz del sol
rt.lights.append(DirectionalLight(direction=[0, -1, 1], intensity=0.8, color=[1.0, 0.8, 0.6]))

# Luz puntual en el sol para emitir luz
rt.lights.append(PointLight(position=[0, 10, -50], intensity=1.0, color=[1.0, 0.9, 0.7]))

# Luces adicionales para resaltar elementos
rt.lights.append(PointLight(position=[-5, 0, -15], intensity=0.5, color=[1.0, 0.8, 0.6]))  # Cerca del árbol 1
rt.lights.append(PointLight(position=[5, 0, -18], intensity=0.5, color=[1.0, 0.8, 0.6]))   # Cerca del árbol 2
rt.lights.append(PointLight(position=[0, -2, -20], intensity=0.3, color=[0.5, 0.5, 1.0]))  # Sobre el lago

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
