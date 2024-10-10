import pygame
from pygame.locals import *
from gl import RendererRT

from figures import *
from material import *
from lights import *
from texture import Texture
from math import radians

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
# Cargar el mapa de entorno (si está disponible)
try:
    rt.envMap = Texture("textures/parkingLot.bmp")
except:
    rt.envMap = None

# Definir materiales con colores para emular texturas
mountain_color = [0.4, 0.3, 0.2]    # Marrón para montañas
tree_trunk_color = [0.55, 0.27, 0.07]  # Marrón oscuro para troncos
leaf_color = [0.2, 0.5, 0.2]        # Verde para hojas
water_color = [0.2, 0.5, 0.7]       # Azul para agua
sun_color = [1.0, 0.9, 0.7]         # Amarillo suave para el sol
rock_color = [0.7, 0.7, 0.7]        # Gris claro para rocas
reflective_color = [0.8, 0.6, 0.2]  # Dorado para materiales reflectivos
refractive_color = [0.9, 0.9, 1.0]  # Color claro para materiales refractivos

# Materiales
mountain_material = Material(diffuse=mountain_color, spec=32, ks=0.1)
tree_trunk_material = Material(diffuse=tree_trunk_color, spec=16, ks=0.2)
leaf_material = Material(diffuse=leaf_color, spec=32, ks=0.3)
water_material = Material(diffuse=water_color, spec=64, ks=0.5, matType=TRANSPARENT, ior=1.33)
rock_material_translucent = Material(diffuse=rock_color, spec=32, ks=0.2, matType=TRANSPARENT, ior=1.5)
sun_material = Material(diffuse=sun_color, spec=0, ks=0.0, matType=EMISSIVE)
reflective_material = Material(diffuse=reflective_color, spec=128, ks=1.0, matType=REFLECTIVE)
refractive_material = Material(diffuse=refractive_color, spec=64, ks=0.5, matType=TRANSPARENT, ior=1.5)

# Limpiar la escena
rt.scene = []

# Crear el paisaje

# Montañas en el fondo (asegurando orientación correcta)
# Montaña izquierda (pirámide reflectiva)
mountain_left = Pyramid(
    base_center=[-15, -5, -50],
    base_size=20,
    height=25,
    material=reflective_material
)
rt.scene.append(mountain_left)

# Montaña derecha (cono refractivo)
mountain_right = Cone(
    position=[15, -5, -55],
    radius=15,
    height=30,
    material=refractive_material
)
rt.scene.append(mountain_right)

# Montaña central (pirámide reflectiva)
mountain_center = Pyramid(
    base_center=[0, -5, -60],
    base_size=25,
    height=35,
    material=reflective_material
)
rt.scene.append(mountain_center)

# Río (plano transparente)
river = Plane(
    position=[0, -5, 0],
    normal=[0, 1, 0],
    material=water_material
)
rt.scene.append(river)

# Árboles a lo largo de las orillas
tree_positions = [
    [-10, -5, -20],
    [-12, -5, -30],
    [-8, -5, -40],
    [10, -5, -25],
    [12, -5, -35],
    [8, -5, -45]
]

for pos in tree_positions:
    trunk = Cylinder(
        position=[pos[0], pos[1], pos[2]],
        radius=0.5,
        height=5,
        material=tree_trunk_material
    )
    rt.scene.append(trunk)

    leaves = Sphere(
        position=[pos[0], pos[1] + 6, pos[2]],
        radius=2,
        material=leaf_material
    )
    rt.scene.append(leaves)

# Rocas translúcidas
rock_positions = [
    [-5, -5.5, -15],
    [0, -5.5, -25],
    [5, -5.5, -35]
]

for pos in rock_positions:
    rock = Ellipsoid(
        position=pos,
        radii=[2, 1.5, 1],
        material=rock_material_translucent
    )
    rt.scene.append(rock)

# Figuras adicionales con materiales reflectivos y refractivos

# Esfera refractiva (gema)
gem = Sphere(
    position=[-3, -4, -20],
    radius=1.5,
    material=refractive_material
)
rt.scene.append(gem)

# Esfera reflectiva (esfera metálica)
metal_sphere = Sphere(
    position=[3, -4, -22],
    radius=1.5,
    material=reflective_material
)
rt.scene.append(metal_sphere)

# Cono reflectivo (árbol estilizado)
stylized_tree = Cone(
    position=[-7, -5, -18],
    radius=2,
    height=6,
    material=reflective_material
)
rt.scene.append(stylized_tree)

# Pirámide refractiva (cristal)
crystal_pyramid = Pyramid(
    base_center=[7, -5, -26],
    base_size=4,
    height=6,
    material=refractive_material
)
rt.scene.append(crystal_pyramid)

# Sol naciente
sun = Sphere(
    position=[0, 10, -100],
    radius=8,
    material=sun_material
)
rt.scene.append(sun)

# Agregar luces
# Luz ambiental con tono cálido
rt.lights.append(AmbientLight(intensity=0.3, color=[1.0, 0.8, 0.6]))

# Luz direccional simulando el sol naciente
rt.lights.append(DirectionalLight(direction=[0, -1, 1], intensity=0.8, color=[1.0, 0.9, 0.7]))

# Luz puntual en el sol
rt.lights.append(PointLight(position=[0, 10, -100], intensity=1.0, color=[1.0, 0.9, 0.7]))

# Luces adicionales con distintos colores y matices
rt.lights.append(PointLight(position=[-10, 0, -20], intensity=0.5, color=[0.8, 0.6, 1.0]))  # Luz violeta
rt.lights.append(PointLight(position=[10, 0, -25], intensity=0.5, color=[0.6, 1.0, 0.8]))   # Luz verde
rt.lights.append(PointLight(position=[0, -2, -30], intensity=0.5, color=[1.0, 0.5, 0.5]))   # Luz roja
rt.lights.append(PointLight(position=[-5, 5, -20], intensity=0.7, color=[0.5, 0.5, 1.0]))   # Luz azul
rt.lights.append(PointLight(position=[5, 5, -20], intensity=0.7, color=[1.0, 1.0, 0.5]))    # Luz amarilla

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
