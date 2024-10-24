import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture
from model import Model

width = 1024
height = 768

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

# Fondo del bosque
try:
    rt.envMap = Texture("textures/woods_background.bmp")
except:
    rt.envMap = None

# Materiales
tree_trunk_material = Material(diffuse=[0.55, 0.27, 0.07], spec=16, ks=0.3)
leaf_material = Material(diffuse=[0.2, 0.6, 0.2], spec=32, ks=0.4)
tent_material = Material(diffuse=[0.7, 0.2, 0.2], spec=64, ks=0.5)
firewood_material = Material(diffuse=[0.5, 0.3, 0.2], spec=32, ks=0.1)
fire_material = Material(diffuse=[1.0, 0.5, 0.1], spec=0, ks=0.1, matType=EMISSIVE)

# Suelo del bosque
ground_material = Material(diffuse=[0.3, 0.25, 0.2], spec=32, ks=0.1)
ground = Plane(position=[0, -5, -20], normal=[0, 1, 0], material=ground_material)
rt.scene.append(ground)

# Posiciones de árboles cercanos y lejanos
tree_positions = [
    [-20, -5, -40], [-15, -5, -30], [-10, -5, -25], [-18, -5, -35],
    [15, -5, -40], [12, -5, -25], [18, -5, -32], [20, -5, -50],
    [-12, -5, -15], [10, -5, -10], [5, -5, -22], [8, -5, -35]
]

# Crear árboles (pinos y follajes variados)
for i, pos in enumerate(tree_positions):
    height = 8 if i % 2 == 0 else 10  # Alternar entre árboles más altos y más bajos
    trunk = Cylinder(position=[pos[0], pos[1], pos[2]], radius=1.0, height=height, material=tree_trunk_material)
    leaves_radius = 3 if i % 2 == 0 else 4
    leaves = Sphere(position=[pos[0], pos[1] + height, pos[2]], radius=leaves_radius, material=leaf_material)
    rt.scene.append(trunk)
    rt.scene.append(leaves)

# Ajuste de la tienda de acampar (más cerca de la fogata y en perspectiva)
tent_main = Pyramid(base_center=[-2, -5, -12], base_size=5, height=5, material=tent_material)
rt.scene.append(tent_main)

# Tiendas adicionales para dar profundidad
tent_far1 = Pyramid(base_center=[-15, -5, -30], base_size=6, height=5, material=tent_material)
tent_far2 = Pyramid(base_center=[10, -5, -25], base_size=6, height=5, material=tent_material)
rt.scene.append(tent_far1)
rt.scene.append(tent_far2)

# Fogata (troncos y fuego)
firewood_positions = [
    [-1, -5, -10], [1, -5, -10], [0, -5, -11],
    [0, -5, -9], [-1.5, -5, -10], [1.5, -5, -10]
]

for pos in firewood_positions:
    firewood = Cylinder(position=[pos[0], pos[1], pos[2]], radius=0.2, height=2, material=firewood_material)
    rt.scene.append(firewood)

fire = Sphere(position=[0, -4.5, -10], radius=0.5, material=fire_material)
rt.scene.append(fire)

# Equipamiento adicional (mochilas junto a las tiendas)
backpack = AABB(position=[-3, -5, -13], sizes=[0.8, 1, 0.5], material=Material(diffuse=[0.3, 0.3, 0.3], spec=32, ks=0.2))
rt.scene.append(backpack)

# Crear un conejo geométrico con figuras simples
rabbit_body = Sphere(position=[4, -5, -18], radius=0.8, material=Material(diffuse=[0.8, 0.8, 0.8], spec=64, ks=0.3))
rabbit_head = Sphere(position=[4, -4, -18], radius=0.5, material=Material(diffuse=[0.8, 0.8, 0.8], spec=64, ks=0.3))
rabbit_ear_left = Cylinder(position=[3.7, -3, -18], radius=0.1, height=0.8, material=Material(diffuse=[0.8, 0.8, 0.8], spec=64, ks=0.3))
rabbit_ear_right = Cylinder(position=[4.3, -3, -18], radius=0.1, height=0.8, material=Material(diffuse=[0.8, 0.8, 0.8], spec=64, ks=0.3))

rt.scene.append(rabbit_body)
rt.scene.append(rabbit_head)
rt.scene.append(rabbit_ear_left)
rt.scene.append(rabbit_ear_right)

# Banana OBJ
# banana_model = Model("models/banana.obj")
# banana_model.translate = [6, -4.5, -20]
# banana_model.scale = [0.5, 0.5, 0.5]
# banana_model.material = Material(diffuse=[1.0, 0.9, 0.0], spec=64, ks=0.3)
# rt.scene.append(banana_model)

# Iluminación: rayos de luz, luz ambiental y fogata
rt.lights.append(DirectionalLight(direction=[-1, -1, 1], intensity=0.9, color=[1.0, 0.9, 0.7]))  # Luz cálida del sol
rt.lights.append(AmbientLight(intensity=0.3, color=[0.7, 0.8, 1.0]))  # Luz ambiental azulada

# Rayos de luz (SpotLights) para los rayos solares
sunlight_angles = [
    SpotLight(position=[-10, 20, -30], direction=[0, -1, 0.3], intensity=1.5, innerAngle=15, outerAngle=30, color=[1.0, 0.7, 0.4]),
    SpotLight(position=[10, 20, -35], direction=[0, -1, 0.3], intensity=1.2, innerAngle=10, outerAngle=25, color=[1.0, 0.6, 0.3])
]

for light in sunlight_angles:
    rt.lights.append(light)

# Luz para la fogata
rt.lights.append(PointLight(position=[0, -4, -10], intensity=1.2, color=[1.0, 0.5, 0.3]))

# Luces adicionales con colores variados
rt.lights.append(PointLight(position=[-15, 5, -30], intensity=0.8, color=[0.8, 0.7, 1.0]))  # Luz violeta
rt.lights.append(PointLight(position=[10, 5, -20], intensity=0.8, color=[0.6, 0.9, 0.8]))   # Luz verde
rt.lights.append(PointLight(position=[5, 5, -22], intensity=0.6, color=[1.0, 0.5, 0.5]))   # Luz roja
rt.lights.append(PointLight(position=[-5, 5, -15], intensity=0.6, color=[0.5, 0.5, 1.0]))  # Luz azul

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
