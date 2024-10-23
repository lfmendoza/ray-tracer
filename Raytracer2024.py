import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture
from model import Model
from math import radians

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
# Cargar el mapa de entorno
rt.envMap = Texture("textures/parkingLot.bmp")

# Definir materiales con colores y texturas
grass_texture = Texture("textures/grass.bmp")
stone_texture = Texture("textures/stone.bmp")
metal_texture = Texture("textures/metal.bmp")
wood_texture = Texture("textures/wood.bmp")

# Materiales
grass_material = Material(spec=32, ks=0.5, texture=grass_texture)
stone_material = Material(spec=32, ks=0.3, texture=stone_texture)
metal_material = Material(spec=128, ks=1.0, matType=REFLECTIVE, texture=metal_texture)
glass_material = Material(spec=64, ks=0.5, matType=TRANSPARENT, ior=1.5)
wood_material = Material(spec=16, ks=0.2, texture=wood_texture)
sun_material = Material(diffuse=[1.0, 0.9, 0.7], spec=0, ks=0.0, matType=EMISSIVE)
water_material = Material(diffuse=[0.2, 0.5, 0.7], spec=64, ks=0.5, matType=TRANSPARENT, ior=1.33)
leaf_material = Material(diffuse=[0.2, 0.5, 0.7], spec=64, ks=0.5, matType=OPAQUE, ior=1.33)

# Limpiar la escena
rt.scene = []

# Añadir figuras al escenario

# Plano de suelo (con textura de césped)
ground = Plane(
    position=[0, -5, 0],
    normal=[0, 1, 0],
    material=grass_material
)
# rt.scene.append(ground)

# Montañas (utilizando la nueva figura Tetrahedron)
mountain_positions = [
    [-20, -5, -50],
    [0, -5, -60],
    [20, -5, -55]
]
for pos in mountain_positions:
    mountain = Tetrahedron(
        position=pos,
        size=20,
        material=stone_material
    )
    rt.scene.append(mountain)

# Lago (plano con material transparente)
lake = Plane(
    position=[0, -5, -30],
    normal=[0, 1, 0],
    material=water_material
)
rt.scene.append(lake)

# Árboles (cilindros y esferas con textura de madera y hojas)
tree_positions = [
    [-15, -5, -20],
    [-10, -5, -25],
    [-5, -5, -22],
    [5, -5, -18],
    [10, -5, -28],
    [15, -5, -24]
]
for pos in tree_positions:
    trunk = Cylinder(
        position=pos,
        radius=0.5,
        height=5,
        material=wood_material
    )
    rt.scene.append(trunk)

    leaves = Sphere(
        position=[pos[0], pos[1] + 6, pos[2]],
        radius=2,
        material=leaf_material
    )
    rt.scene.append(leaves)

# Rocas translúcidas (usando la nueva figura Prism)
rock_positions = [
    [-5, -5, -15],
    [0, -5, -25],
    [5, -5, -35]
]
for pos in rock_positions:
    rock = Prism(
        position=pos,
        radius=2,
        height=3,
        sides=6,  # Hexagonal prism
        material=glass_material
    )
    rt.scene.append(rock)

# Esfera reflectiva (usando material con textura de metal)
metal_sphere = Sphere(
    position=[0, -4, -20],
    radius=2,
    material=metal_material
)
rt.scene.append(metal_sphere)

# Modelo OBJ (colocamos un modelo en la escena)
# LFMendoza
# model = Model("models/face.obj")
# model_material = Material(spec=64, ks=0.5, texture=stone_texture)
# model.position = [0, -5, -30]
# model.scale = [0.5, 0.5, 0.5]
# model.material = model_material
# rt.scene.append(model)

# Sol (emisivo)
sun = Sphere(
    position=[0, 20, -100],
    radius=10,
    material=sun_material
)
rt.scene.append(sun)

# Agregar luces
rt.lights.append(AmbientLight(intensity=0.2, color=[1.0, 1.0, 1.0]))
rt.lights.append(DirectionalLight(direction=[0, -1, 1], intensity=0.8, color=[1.0, 0.95, 0.9]))
rt.lights.append(PointLight(position=[0, 20, -100], intensity=1.0, color=[1.0, 0.9, 0.7]))

# Luces adicionales
rt.lights.append(SpotLight(position=[-10, 0, -20], direction=[1, -1, 0], intensity=0.5, color=[0.8, 0.6, 1.0], innerAngle=30, outerAngle=45))
rt.lights.append(SpotLight(position=[10, 0, -25], direction=[-1, -1, 0], intensity=0.5, color=[0.6, 1.0, 0.8], innerAngle=30, outerAngle=45))

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
