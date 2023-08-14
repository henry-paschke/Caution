import pygame as pg
import math
import vector_math

class Game_object:
    def __init__(self, position, rotation_radians, length, name):
        self.local_position = position
        self.local_rotation = rotation_radians
        self.parent = None
        self.global_position = [0,0]
        self.global_rotation = 0
        self.length = length
        self.name = name
        self.children = []

    def add_child(self, game_object):
        self.children.append(game_object)
        game_object.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def chain_update(self, surface):
        self.global_rotation = self.parent.global_rotation + self.local_rotation
        self.global_position = vector_math.get_endpos(self.parent.global_position, self.parent.global_rotation, self.local_position[0], self.local_position[1])
        self.normalize_rotation()
        pg.draw.line(surface, (255,255,255), self.global_position, vector_math.get_endpos(self.global_position, self.global_rotation, self.length, 0))
        for child in self.children:
            child.chain_update(surface)

    #TODO remove duplicate code 
    def update(self, surface):
        self.global_position = vector_math.add_vector2([0,0], self.local_position)
        self.global_rotation = self.local_rotation
        self.normalize_rotation()
        pg.draw.line(surface, (255,255,255), self.global_position, vector_math.get_endpos(self.global_position, self.global_rotation, self.length, 0))
        for child in self.children:
            child.chain_update(surface)
    
    def normalize_rotation(self):
        self.local_rotation = vector_math.normalize_radian_angle(self.local_rotation)
        self.global_rotation = vector_math.normalize_radian_angle(self.global_rotation)
    
    def get_visualization(self):
        visual = self.name
        if (len(self.children)):
            visual += "("
            for i in range(len(self.children)):
                visual += (self.children[i].get_visualization())
                if (i != len(self.children)):
                    visual + ", "
            visual += ")"
        return visual
    
    def serialize_data(self):
        return [self.local_position[0], self.local_position[1], self.length, self.local_rotation]
