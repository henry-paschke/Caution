import pygame as pg
import math
import vector_math

class Game_object:
    def __init__(self, position, rotation_radians, length, image):
        self.local_position = position
        self.local_rotation = rotation_radians
        self.parent = None
        self.global_position = [0,0]
        self.global_rotation = 0
        self.length = length
        self.image = image
        self.children = []

    def add_child(self, game_object):
        self.children.append(game_object)

    def set_parent(self, parent):
        self.parent = parent

    def get_global_endpos(self):
        return vector_math.get_endpos(self.global_position, self.global_rotation, self.length)

    def chain_update(self, surface):
        self.global_position = vector_math.add_vector2(self.parent.get_global_endpos(), self.local_position)
        self.global_rotation = self.parent.global_rotation + self.local_rotation
        self.normalize_rotation()
        pg.draw.line(surface, (255,255,255), self.global_position, self.get_global_endpos())
        for child in self.children:
            child.chain_update(surface)

    def update(self, surface):
        self.normalize_rotation()
        pg.draw.line(surface, (255,255,255), self.global_position, self.get_global_endpos())
        for child in self.children:
            child.chain_update(surface)
    
    def normalize_rotation(self):
        self.local_rotation = vector_math.normalize_radian_angle(self.local_rotation)
        self.global_rotation = vector_math.normalize_radian_angle(self.global_rotation)