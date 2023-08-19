import pygame as pg

import game_object
import utility
import keyframe_animation
import animation_data

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

    def update(self, surface, d_t, position):
        self.surf.fill((0,0,0,0))
        self.go.update(self.surf, d_t, [-300,0])
        self.animation.update(d_t)

        surface.blit(self.surf, position)

    def switch_animation(self, name):
        t = pg.time.get_ticks()
        if name != self.current:
            self.animation.switch_animation(self.animation_data[name])
            self.current = name
        print(pg.time.get_ticks() - t)



