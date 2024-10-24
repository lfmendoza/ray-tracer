import random
from PIL import Image, ImageDraw, ImageFilter
import os

def generate_wood_texture(filename, width=512, height=512):
    image = Image.new("RGB", (width, height), (139, 69, 19))  # Color base marrón
    draw = ImageDraw.Draw(image)

    # Añadir vetas de madera
    for i in range(0, width, 4):
        line_color = (int(139 + (i % 20)), int(69 + (i % 10)), int(19 + (i % 5)))
        draw.line([(i, 0), (i, height)], fill=line_color)

    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    image.save(filename)

def generate_carpet_texture(filename, width=512, height=512):
    image = Image.new("RGB", (width, height), (200, 0, 0))  # Color base rojo
    draw = ImageDraw.Draw(image)

    # Añadir patrón de puntos
    for y in range(0, height, 20):
        for x in range(0, width, 20):
            color_variation = int((x * y) % 50)
            draw.ellipse([(x, y), (x+10, y+10)], fill=(200 - color_variation, 0, 0))

    image.save(filename)

def generate_metal_texture(filename, width=512, height=512):
    image = Image.new("RGB", (width, height), (192, 192, 192))  # Gris metálico
    draw = ImageDraw.Draw(image)

    # Añadir líneas para simular metal cepillado
    for i in range(0, height, 2):
        line_color = (int(192 + (i % 10)), int(192 + (i % 10)), int(192 + (i % 10)))
        draw.line([(0, i), (width, i)], fill=line_color)

    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    image.save(filename)

def generate_room_envmap(filename, width=512, height=512):
    # Cambiar el fondo para un arcade room
    image = Image.new("RGB", (width, height), (0, 0, 0))  # Fondo negro
    draw = ImageDraw.Draw(image)

    # Añadir luces de neón simuladas
    for i in range(10):
        x = i * 50
        color = (255, 0, 255) if i % 2 == 0 else (0, 255, 255)
        draw.line([(x, 0), (x, height)], fill=color, width=5)

    image = image.filter(ImageFilter.GaussianBlur(radius=2))
    image.save(filename)

def generate_arcade_machine_texture(filename, width=512, height=512):
    image = Image.new("RGB", (width, height), (50, 50, 50))  # Gris oscuro
    draw = ImageDraw.Draw(image)

    # Añadir botones y pantalla
    draw.rectangle([(50, 50), (width - 50, height - 150)], fill=(0, 0, 255))  # Pantalla azul
    draw.ellipse([(100, height - 130), (130, height - 100)], fill=(255, 0, 0))  # Botón rojo
    draw.ellipse([(150, height - 130), (180, height - 100)], fill=(0, 255, 0))  # Botón verde
    draw.ellipse([(200, height - 130), (230, height - 100)], fill=(0, 0, 255))  # Botón azul

    image.save(filename)

def generate_banana_texture(filename, width=512, height=512):
    image = Image.new("RGB", (width, height), (255, 255, 0))  # Amarillo
    draw = ImageDraw.Draw(image)

    # Añadir manchas marrones
    for i in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse([(x, y), (x + 5, y + 5)], fill=(139, 69, 19))

    image.save(filename)

def generate_mario_bros_texture(filename, width=512, height=512):
    image = Image.new("RGB", (width, height), (0, 0, 255))  # Fondo azul
    draw = ImageDraw.Draw(image)

    # Dibujar elementos simples para simular una pantalla de juego
    draw.rectangle([(100, 400), (400, 450)], fill=(0, 255, 0))  # Suelo verde
    draw.rectangle([(200, 350), (250, 400)], fill=(255, 0, 0))  # Personaje rojo
    draw.rectangle([(300, 300), (350, 350)], fill=(255, 255, 0))  # Moneda amarilla

    image.save(filename)

def generate_textures():
    os.makedirs("textures", exist_ok=True)
    generate_wood_texture("textures/wood_floor.bmp")
    generate_wood_texture("textures/wood_table.bmp")
    generate_carpet_texture("textures/carpet.bmp")
    generate_room_envmap("textures/arcade_envmap.bmp")
    generate_arcade_machine_texture("textures/arcade_machine.bmp")
    generate_banana_texture("textures/banana_texture.bmp")
    generate_mario_bros_texture("textures/mario_bros.bmp")
    generate_metal_texture("textures/metal.bmp")

if __name__ == "__main__":
    generate_textures()
    print("Texturas generadas exitosamente.")
