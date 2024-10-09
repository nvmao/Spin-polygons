import colorsys
import math

import pygame as pygame
from pygame import DOUBLEBUF, Vector2

from Sounds import Sounds

width = 720
height = 720

screen = pygame.display.set_mode((width, height), DOUBLEBUF, 16)
surface = pygame.Surface((width,height),pygame.SRCALPHA)

clock = pygame.time.Clock()

def hueToRGB( hue):
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    # Scale RGB values to 0-255 range
    return (int(r * 255), int(g * 255), int(b * 255))


class Polygon:
    def __init__(self,radius,slide,color,rotateSpeed):
        self.center = Vector2(width/2,height/2)
        self.slide = slide
        self.angle = 0
        self.radius = radius
        self.startRadius = radius
        self.rotateSpeed = rotateSpeed
        self.color = color
        self.vertices = []
        for i in range(self.slide):
            angle = i * (2 * math.pi / self.slide)
            x = self.center.x + radius * math.cos(angle)
            y = self.center.y + radius * math.sin(angle)
            self.vertices.append(Vector2(x, y))


    def update(self,time):
        self.angle = -360 + math.sin(time * self.rotateSpeed) * 5
        self.rotateVertices()


    def rotateVertices(self):
        angle_radians = math.radians(self.angle)

        rotated_vertices = []

        for vertex in self.vertices:
            relative_x = vertex.x - self.center.x
            relative_y = vertex.y - self.center.y

            rotated_x = relative_x * math.cos(angle_radians) - relative_y * math.sin(angle_radians)
            rotated_y = relative_x * math.sin(angle_radians) + relative_y * math.cos(angle_radians)

            rotated_vertex = Vector2(rotated_x + self.center.x, rotated_y + self.center.y)

            rotated_vertices.append(rotated_vertex)

        self.vertices = rotated_vertices


    def draw(self):
        pygame.draw.polygon(surface,self.color,self.vertices,2)



#############################################################

objects = []
time = 0
time2 = 0

maxObjects = 50
radius = 50
slide = 8
rotateSpeed = 1
hue = 0
hueStep = 1/maxObjects

for i in range(maxObjects):
    object = Polygon(radius,slide, hueToRGB(hue),rotateSpeed)
    hue += hueStep
    radius += 5
    rotateSpeed *= 0.98

    objects.append(object)


while True:
    surface.fill((0, 0, 0,50), (0, 0, width, height))
    deltaTime = clock.tick(60)/1000

    time2 += deltaTime
    time = math.sin(time2 * 0.2) * math.pi * 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    for object in objects:
        object.update(time)
        object.draw()

    screen.blit(surface,(0,0))
    pygame.display.flip()
