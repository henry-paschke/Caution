import pygame as pg

import game_object
import utility
import keyframe_animation
import animation_data
import vector_math

class Animation_wrapper:
    def __init__(self, skeleton_path, initial_animation_path, assets_list, paths):
        self.go = game_object.create_game_object_from_file(skeleton_path, assets_list)
        self.animation = keyframe_animation.create_animation("animations/" + initial_animation_path + ".anim", self.go)
        self.surf = pg.surface.Surface((500,600)).convert_alpha()
        self.animation_data = {}
        self.animation_data[initial_animation_path] = animation_data.Animation_data("animations/" + initial_animation_path + ".anim")
        for i in paths:
            self.animation_data[str(i)] = animation_data.Animation_data("animations/" + str(i) + ".anim")
        self.current = initial_animation_path
        self.flip = False
        self.offset = [-175, -150]

    def update(self,surface, d_t, rect, ragdoll):
        self.surf.fill((0,0,0,0))
        bl = []
        self.go.update(d_t, bl, [-300,0])
        self.surf.blits(bl)
        self.animation.update(d_t)

        surface.blit(pg.transform.flip(self.surf, self.flip, False), vector_math.add_vector2(rect.topleft, self.offset))
        

    def get_child(self, name):
        return self.go.seek_first_child(name)
    
    def get_child_pos(self, name, draw_rect_pos):
        return vector_math.add_vector2(vector_math.add_vector2(vector_math.add_vector2(draw_rect_pos.topleft, self.offset), [0,0]), self.go.seek_first_child(name).global_position)
        
    def switch_animation(self, name):
        if name != self.current:
            self.animation.switch_animation(self.animation_data[name])
            self.current = name