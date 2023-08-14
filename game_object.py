import pygame as pg
import math
import vector_math

class Target:
    def __init__(self, position : list[float, float], rotation : float, time = -1):
        self.position = position.copy()
        self.rotation = rotation
        self.time = time
    def Xpos(self):
        return self.position[0]
    def Ypos(self):
        return self.position[1]


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
        self.target = None
        self.elapsed = 0
        self.target_startpos = None

    def add_child(self, game_object):
        self.children.append(game_object)
        game_object.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def chain_update(self, surface, delta_time):
        self.update_target(delta_time)
        self.global_rotation = self.parent.global_rotation + self.local_rotation
        self.global_position = vector_math.get_endpos(self.parent.global_position, self.parent.global_rotation, self.local_position[0], self.local_position[1])
        self.normalize_rotation()
        pg.draw.line(surface, (255,255,255), self.global_position, vector_math.get_endpos(self.global_position, self.global_rotation, self.length, 0))
        for child in self.children:
            child.chain_update(surface, delta_time)

    #TODO remove duplicate code 
    def update(self, surface, delta_time):
        self.update_target(delta_time)
        self.global_position = vector_math.add_vector2([0,0], self.local_position)
        self.global_rotation = self.local_rotation
        self.normalize_rotation()
        pg.draw.line(surface, (255,255,255), self.global_position, vector_math.get_endpos(self.global_position, self.global_rotation, self.length, 0))
        for child in self.children:
            child.chain_update(surface, delta_time)

    def update_target(self, delta_time):
        if (self.target):
            if self.elapsed < self.target.time:
                self.elapsed += delta_time
                self.local_position[0] = vector_math.lerp(self.target_startpos.Xpos(), self.target.Xpos(), self.elapsed, self.target.time)
                self.local_position[1] = vector_math.lerp(self.target_startpos.Ypos(), self.target.Ypos(), self.elapsed, self.target.time)
                self.local_rotation = vector_math.lerp(self.target_startpos.rotation, self.target.rotation, self.elapsed, self.target.time)
            else:
                self.local_position[0] = self.target.Xpos()
                self.local_position[1] = self.target.Ypos()
                self.local_rotation = self.target.rotation
                self.target = None

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
        self.normalize_rotation()
        return Target(self.local_position, self.local_rotation)

    def seek_first_child(self, name_string):
        for child in self.children:
            if child.name == name_string:
                return child
            else:
                child_result = child.seek_first_child(name_string)
                if child_result:
                    return child_result
        return False
    
    #targets are in this format: [time, [localposX, localposY], rotation]
    def set_target(self, target):
        self.elapsed = 0
        self.target = target
        self.target_startpos = self.serialize_data()
