from PIL import Image, ImageDraw
import random

def create_grass_texture(size, filename):
    img = Image.new('RGB', (size, size), (34, 139, 34))  # Default grass green
    draw = ImageDraw.Draw(img)
    for _ in range(10000):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        green_variation = random.randint(100, 255)
        draw.point((x, y), fill=(0, green_variation, 0))
    img.save(filename, 'BMP')

def create_stone_texture(size, filename):
    img = Image.new('RGB', (size, size), (128, 128, 128))  # Default grey color
    draw = ImageDraw.Draw(img)
    for _ in range(5000):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        grey_shade = random.randint(100, 200)
        draw.point((x, y), fill=(grey_shade, grey_shade, grey_shade))
    img.save(filename, 'BMP')

def create_metal_texture(size, filename):
    img = Image.new('RGB', (size, size), (192, 192, 192))  # Default metallic color
    draw = ImageDraw.Draw(img)
    for y in range(size):
        for x in range(size):
            shade = 190 + (x % 10) * 6  # Create a brushed metal effect
            draw.point((x, y), fill=(shade, shade, shade))
    img.save(filename, 'BMP')

def create_wood_texture(size, filename):
    img = Image.new('RGB', (size, size), (139, 69, 19))  # Default brown color for wood
    draw = ImageDraw.Draw(img)
    for y in range(size):
        for x in range(size):
            variation = random.randint(-20, 20)
            r = max(0, min(139 + variation, 255))
            g = max(0, min(69 + variation, 255))
            b = max(0, min(19 + variation, 255))
            draw.point((x, y), fill=(r, g, b))
    img.save(filename, 'BMP')

def main():
    size = 256  # Set texture size
    create_grass_texture(size, 'grass_texture.bmp')
    create_stone_texture(size, 'stone_texture.bmp')
    create_metal_texture(size, 'metal_texture.bmp')
    create_wood_texture(size, 'wood_texture.bmp')

if __name__ == "__main__":
    main()
