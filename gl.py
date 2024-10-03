import struct
from camera import Camera
from math import tan, pi, atan2, acos
from MathLib import dot, sub, add, mul, norm, length
import pygame
import random

def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    # 2 bytes
    return struct.pack("=h", w)

def dword(d):
    # 4 bytes
    return struct.pack("=l", d)

MAX_RECURSION_DEPTH = 3

class RendererRT(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

        self.scene = []
        self.lights = []

        self.envMap = None

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = width
        self.vpHeight = height

    def glProjection(self, n=0.1, f=1000, fov=60):
        self.nearPlane = n
        self.farPlane = f
        self.fov = fov * pi / 180

        aspectRatio = self.vpWidth / self.vpHeight

        self.topEdge = tan(self.fov / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [r, g, b]

    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r, g, b]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor[:] for x in range(self.width)]
                            for y in range(self.height)]

    def glEnvMapColor(self, orig, dir):
        if self.envMap:
            x = (atan2(dir[2], dir[0]) / (2 * pi) + 0.5)
            y = acos(-dir[1]) / pi

            return self.envMap.getColor(x, y)

        return self.clearColor

    def glPoint(self, x, y, color=None):
        x = int(round(x))
        y = int(round(y))

        if (0 <= x < self.width) and (0 <= y < self.height):
            color = color or self.currColor
            color_int = [int(min(1, max(0, c)) * 255) for c in color]

            # Invertir el eje y al dibujar con Pygame
            self.screen.set_at((x, self.height - 1 - y), color_int)

            # Almacenar el píxel en el framebuffer con el eje y invertido
            self.frameBuffer[self.height - 1 - y][x] = color

    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Pixel data
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[y][x]
                    color_bytes = bytes([int(color[2] * 255),
                                         int(color[1] * 255),
                                         int(color[0] * 255)])
                    file.write(color_bytes)

    def glCastRay(self, orig, direction, sceneObj=None, recursion=0):
        if recursion >= MAX_RECURSION_DEPTH:
            return None

        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if obj != sceneObj:
                intercept = obj.ray_intersect(orig, direction)
                if intercept is not None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        return hit

    def glRender(self):
        indices = [(i, j) for i in range(self.vpX, self.vpX + self.vpWidth)
                   for j in range(self.vpY, self.vpY + self.vpHeight)]
        random.shuffle(indices)

        for x, y in indices:
            # Coordenadas normalizadas
            # Que van de -1 a 1

            pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
            pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

            pX *= self.rightEdge
            pY *= self.topEdge

            dir = [pX, pY, -self.nearPlane]
            dir = norm(dir)

            intercept = self.glCastRay(self.camera.translate, dir)
            color = [0, 0, 0]

            if intercept is not None:
                color = intercept.obj.material.GetSurfaceColor(intercept, self)
            else:
                color = self.glEnvMapColor(self.camera.translate, dir)

            self.glPoint(x, y, color)
        pygame.display.flip()
