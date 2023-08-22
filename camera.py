import pygame as pg
import vector_math

class Camera:
    def __init__(self, size):
        self.surface = pg.surface.Surface(size)
        self.position = [0,0]
        self.size = size

    def blit(self, surface, position):
        self.surface.blit(surface, vector_math.add_vector2(position, [-self.position[0], -self.position[1]]))
    
    def draw_rect(self, rect, color):
        pg.draw.rect(self.surface, color, (rect.x - self.position[0], rect.y - self.position[1], rect.width, rect.height))
    
    def target(self, pos):
        speed = .5
        x = vector_math.lerp(self.position[0], pos[0] - self.size[0] / 3, speed, 1)
        y = vector_math.lerp(self.position[1], pos[1] - self.size[1] / 3, speed, 1)
        self.position = [x , y]
