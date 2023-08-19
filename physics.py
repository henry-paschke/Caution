#hi this is the physics engine!!!!!!!!!!!!!!!
#OMG
import pygame as pg
import math

RED = (255, 0, 0)


class Physics_object:

    def __init__(self, x, y, w, h, weight):
        self.hitbox = pg.rect.Rect(x, y, w, h)
        self.velocity = [0, 0]
        self.weight = weight
        self.grounded = False
        self.impact = False
    
    def draw(self, screen):
        pg.draw.rect(screen, RED, self.hitbox)

    def update(self, d_time):
        if self.grounded == False:
            gravity = 0.000981
            self.velocity[1] += gravity * d_time * self.weight
        

    def collide_with_objects(self, hitbox_list, d_time):
        bounce = 0.7
        if self.grounded == False:
            self.hitbox.y += self.velocity[1] * d_time

            hitlist = self.get_hit_list(hitbox_list)
            for other_hitbox in hitlist:
                if self.velocity[1] > 0:
                    self.hitbox.bottom = other_hitbox.top
                else:
                    self.hitbox.top = other_hitbox.bottom
            if len(hitlist):
                self.velocity[1] = -self.velocity[1] * bounce
                self.impact = True
                if abs(self.velocity[1]) < 0.3:
                    self.velocity[1] = 0
                    self.grounded = True
                    self.impact = False

        self.hitbox.x += self.velocity[0] * d_time

        hitlist = self.get_hit_list(hitbox_list)
        for other_hitbox in hitlist:
            if self.velocity[0] > 0:
                self.hitbox.right = other_hitbox.left
            else:
                self.hitbox.left = other_hitbox.right
        if len(hitlist):
            self.impact = True
            self.velocity[0] = -self.velocity[0] * bounce
            self.velocity[1] = -self.velocity[1] * bounce

        
        #print(self.velocity)
        

    def get_hit_list(self, hitboxes):
        hit_list = []
        for hit in hitboxes:
            if (self.hitbox.colliderect(hit)):
                hit_list.append(hit)
        return hit_list

