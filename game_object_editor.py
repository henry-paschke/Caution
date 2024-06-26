import pygame as pg
import math
import vector_math
from globals import *
import utility

class Target:
    def __init__(self, position : list[float, float], rotation : float, time = -1):
        self.position = list(position).copy()
        self.rotation = rotation
        self.time = time
    def Xpos(self):
        return self.position[0]
    def Ypos(self):
        return self.position[1]
    
def create_keyframe_from_serialized(data, time):
    target = Target(data[0], data[1], time)
    output = [target, []]
    for i in range(len(data[2])):
        output[1].append(create_keyframe_from_serialized(data[2][i], time))
    return output

def create_game_object_from_structure_list(structure_list):
    go = Game_object([0,0], 0, 100, structure_list[0], None)
    for entry in structure_list[1]:
        go.add_child(create_game_object_from_structure_list(entry))
    return go

def create_game_object_from_file(fp, assets):
    structure = utility.read_from_json(fp)
    go = create_game_object_from_structure_list(structure["armature"])
    texture_path = structure["path"]
    texture = pg.image.load(texture_path)
    assets.append(texture)
    size = structure["size"]
    texture_list = []
    for i in range(int(texture.get_width() / size)):
        texture_list.append(texture.subsurface( i*size, 0, size, size))
    go.apply_image_list(structure["image_references"], texture_list)
    return go


class Game_object:
    def __init__(self, position, rotation_radians, length, name, img):
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
        self.selected = False
        self.img = img

    def add_child(self, game_object):
        self.children.append(game_object)
        game_object.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def chain_update(self, surface, delta_time, target_update):
        if (target_update):
            self.update_target(delta_time)
        self.global_rotation = self.parent.global_rotation + self.local_rotation
        self.global_position = vector_math.get_endpos(self.parent.global_position, self.parent.global_rotation, -self.local_position[0], -self.local_position[1])
        self.normalize_rotation()
        self.draw(surface)
        for child in self.children:
            child.chain_update(surface, delta_time, target_update)

    #TODO remove duplicate code 
    def update(self, surface, delta_time, target_update):
        if (target_update):
            self.update_target(delta_time)
        self.global_position = vector_math.add_vector2([0,0], self.local_position)
        self.global_rotation = self.local_rotation
        self.normalize_rotation()
        self.draw(surface)
        for child in self.children:
            child.chain_update(surface, delta_time, target_update)

    def update_target(self, delta_time):
        if (self.target):
            if self.elapsed < self.target.time:
                self.elapsed += delta_time
                self.local_position[0] = vector_math.lerp(self.target_startpos.Xpos(), self.target.Xpos(), self.elapsed, self.target.time)
                self.local_position[1] = vector_math.lerp(self.target_startpos.Ypos(), self.target.Ypos(), self.elapsed, self.target.time)
                self.local_rotation = vector_math.angular_lerp(self.target_startpos.rotation, self.target.rotation, self.elapsed, self.target.time)
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
                if (i != len(self.children) - 1):
                    visual += ", "
            visual += ")"
        return visual
    
    def get_current_as_target(self):
        self.normalize_rotation()
        return Target(self.local_position, self.local_rotation)
    
    def serialize_data(self):
        self.normalize_rotation()
        data = [self.local_position, self.local_rotation, []]
        for child in self.children:
            data[2].append(child.serialize_data())
        return data
    
    def read_serialized_data(self, data):
        self.local_position = data[0].copy()
        self.local_rotation = data[1]
        for i in range(len(data[2])):
            self.children[i].read_serialized_data(data[2][i].copy())

    def seek_first_child(self, name_string):
        for child in self.children:
            if child.name == name_string:
                return child
            else:
                child_result = child.seek_first_child(name_string)
                if child_result:
                    return child_result
        return False
    
    def seek_selected(self):
        if self.selected:
            return self
        for child in self.children:
            if child.selected:
                return child
            else:
                child_result = child.seek_selected()
                if child_result:
                    return child_result
        return False
    

    #targets are in this format: [time, [localposX, localposY], rotation]
    def set_target(self, target):
        self.elapsed = 0
        self.target = target
        self.target_startpos = self.get_current_as_target()

    def set_keyframe(self, keyframe):
        self.set_target(keyframe[0])
        for i in range(len(keyframe[1])):
            self.children[i].set_keyframe(keyframe[1][i])

    def draw_recursive(self, surface):
        self.draw(surface)
        for child in self.children:
            child.draw_recursive(surface)
    
    def draw(self, surface):
        if (self.img):
            rotatedimg = pg.transform.rotate(self.img, -vector_math.radians_to_degrees(self.global_rotation))
            surface.blit(rotatedimg, vector_math.add_vector2(self.global_position, (-rotatedimg.get_width() / 2, -rotatedimg.get_height() / 2)))
        
        if self.selected:
            pg.draw.line(surface, (255,0,0), self.global_position, vector_math.get_endpos(self.global_position, self.global_rotation, self.length, 0), 5)
        else :
            pg.draw.line(surface, (0,255,0), self.global_position, vector_math.get_endpos(self.global_position, self.global_rotation, self.length, 0), 3)
    
    def select_parent(self):
        if self.parent:
            self.parent.selected = True
            self.selected = False
            return self.parent
        console_log("No parent of selected object " + self.name)
        return self

    def select_first_child(self):
        if len(self.children):
            self.selected = False
            self.children[0].selected = True
            return self.children[0]
        else:
            console_log("No children of selected object " + self.name)
            return self
        

    def select_sibling(self):
        if self.parent:
            index = self.parent.children.index(self)
            index += 1
            if index >= len(self.parent.children):
                index = 0
            self.selected = False
            self.parent.children[index].selected = True
            return self.parent.children[index]
        console_log("No sibling of selected object " + self.name)
        return self
            
    def get_structure_list(self):
        data = [self.name, []]
        for child in self.children:
            data[1].append(child.get_structure_list())
        return data

    def apply_image_list(self, img_list, textures):
        if img_list[0] != None:
            self.img = textures[img_list[0]]
        for i in range(len(img_list[1])):
            self.children[i].apply_image_list(img_list[1][i], textures)
            