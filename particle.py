import pygame as pg
import vector_math
import physics
import random


class Particle:
    def __init__(self, img, pos, rotation, weight, vel):
        self.img = img.subsurface((img.get_width() / 3.0, img.get_width() / 4.0, img.get_width() / 3.0 * 2.0, img.get_width() / 2.0))
        self.rot = rotation
        self.rot_vel = random.randint(0, 4) / 400
        self.physics_body = physics.Physics_object(pos[0], pos[1], self.img.get_width(), self.img.get_width() / 2.0, weight)
        self.physics_body.velocity = vector_math.add_vector2(vel, [(random.randint(0, 2) - 1) / 4, (random.randint(0, 2) - 1) / 4])
        self.dead = False
    
    def update(self, surface, hitboxes, d_t):
        self.physics_body.update(d_t)
        self.physics_body.collide_with_objects(hitboxes, d_t)
        self.draw(surface)
        if self.physics_body.grounded == False:
            self.rot += self.rot_vel * d_t
        else: 
            self.physics_body.velocity[0] = 0

    def draw(self, surface):
        rotatedimg = pg.transform.rotate(self.img, -vector_math.radians_to_degrees(self.rot))
        surface.blit(rotatedimg, vector_math.add_vector2((self.physics_body.hitbox.centerx, self.physics_body.hitbox.bottom), (-rotatedimg.get_width() / 2, -rotatedimg.get_height() / 2)))

BLOOD_RANDOM = 10

class Blood:
    def __init__(self, pos, vel=None):
        self.pos = pos
        self.physics_body = physics.Physics_object(pos[0], pos[1], 4,4, 3)
        if vel == None:
            self.physics_body.velocity = [(random.randint(0, BLOOD_RANDOM * 2) - BLOOD_RANDOM) / 4, (random.randint(0, BLOOD_RANDOM * 2) - BLOOD_RANDOM) / 4]
        else:
            self.physics_body.velocity = vector_math.add_vector2(vel , [(random.randint(0, BLOOD_RANDOM) - BLOOD_RANDOM/2) / 8, (random.randint(0, BLOOD_RANDOM) - BLOOD_RANDOM/2) / 8])
        self.dead = False
    
    def update(self, surface, hitboxes, d_t):
        self.physics_body.update(d_t)
        self.physics_body.collide_with_objects([], d_t)
        surface.draw_rect(self.physics_body.hitbox, (255,0,0))
        if self.physics_body.hitbox.y > 3000:
            self.dead = True

def remove_dead_objects(objects):
    i = 0
    while i < len(objects):
        if objects[i].dead:
            # Swap with the last object and pop
            objects[i], objects[-1] = objects[-1], objects[i]
            objects.pop()
        else:
            i += 1