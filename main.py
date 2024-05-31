import pygame as pg
pg.init()

import utility
import animation_wrapper
import physics
import camera
import particle
import vector_math
import math


#python -m cProfile -o main.prof main.py   
#python -m snakeviz main.prof -b windows-default

#constants
RES_SCALE = 2
SCREEN_SIZE = (960 * RES_SCALE, 540 * RES_SCALE)
BLACK  = (0,0,0)
WHITE = (255,255,255)
SCREEN_LABEL = "CAUTION"

g_running = True
g_screen_surface = camera.Camera(SCREEN_SIZE)
info_object = pg.display.Info()
#WINDOW_SIZE = (info_object.current_w, info_object.current_h)
WINDOW_SIZE = ((info_object.current_w / 2, info_object.current_h / 2))
g_window = pg.display.set_mode(WINDOW_SIZE, pg.SCALED | pg.RESIZABLE)
pg.display.set_caption(SCREEN_LABEL)
g_clock = pg.time.Clock()
g_debug_font = pg.font.Font(None, 20)
g_particles = []
g_speed = 1.0
g_zoom = 1.0

death_stamp = 0
font = pg.font.Font("font/safety/SafetyMedium.otf")
death_label = font.render("You died. Press f to restart.", (0,0,0, 255), (0,0,0,0))


g_assets = []

go = animation_wrapper.Animation_wrapper("skeletons/human.ske", "tumble", g_assets, ["walk", "idle", "jump", "rocket", "pound"])

player_body = physics.Physics_object(0,0,150,350, 4)

leak_spots = []

floors = [
    pg.rect.Rect(0, 900, 100000, 500),
    pg.rect.Rect(1500, 0, 500, 1000),
    pg.rect.Rect(3000, 250, 250, 1000)
]

traps = [
    pg.rect.Rect(900, 900 - 64, 64,64)
]

spike = pg.image.load("spike.png")


while g_running:
    g_screen_surface.surface.fill(WHITE)
    d_t = g_clock.tick_busy_loop(300) / g_speed
    
    utility.stamp_text([str(g_clock.get_fps())], g_screen_surface, (20,20))

    g_screen_surface.blit(spike, traps[0].topleft)

    player_body.update(d_t)
    player_body.collide_with_objects(floors, d_t)
    for f in floors:
        g_screen_surface.draw_rect(f, (0,0,0))

    for i in range(len(g_particles)):
        g_particles[i].update(g_screen_surface, floors, d_t)

    particle.remove_dead_objects(g_particles)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            g_running = False
            pg.quit()
            quit()
        if (e.type == pg.KEYDOWN):
            if e.key == pg.K_ESCAPE:
                g_running = False
                pg.quit()
                quit()
            if e.key == pg.K_SPACE and player_body.impact == False:
                player_body.velocity[1] = -1
                player_body.grounded = False
                go.switch_animation("jump")
            if e.key == pg.K_f:
                player_body = physics.Physics_object(0,0,150,350,4)     
                go.go.set_visible()   
                g_speed = 1
                g_zoom = 1
                death_stamp = 0
                leak_spots.clear()
            if e.key == pg.K_e and player_body.grounded == False:
                if not go.flip:
                    player_body.velocity[0] = 1.5
                else :
                    player_body.velocity[0] = -1.5
                player_body.velocity[1] = -0.5
                go.switch_animation("rocket")   
            if e.key == pg.K_q and player_body.grounded == False:
                player_body.velocity[1] = 2
                go.switch_animation("pound")  
            if e.key == pg.K_9:
                go.get_child("Head").gib(g_particles, [player_body.hitbox.x - 200, player_body.hitbox.y -150], player_body.velocity)
                leak_spots.append("Head")
                go.get_child("Left_arm_bottom").gib(g_particles, [player_body.hitbox.x - 200, player_body.hitbox.y -150], player_body.velocity)
                leak_spots.append("Left_arm_bottom")
        
    if (player_body.impact and player_body.grounded == False):       
        go.switch_animation("tumble")           
       
    k = pg.key.get_pressed()       
    if (k[pg.K_d] and player_body.impact == False):       
        if player_body.grounded:       
            go.switch_animation("walk")       
            go.flip = False       
        if player_body.velocity[0] > 0:       
            player_body.velocity[0] = player_body.velocity[0] + 0.0007 * d_t       
        else:       
            player_body.velocity[0] = .3       
    elif (k[pg.K_a] and player_body.impact == False):       
        if player_body.grounded:       
            go.switch_animation("walk")       
            go.flip = True
        if player_body.velocity[0] < 0:
            player_body.velocity[0] = player_body.velocity[0] - 0.0007 * d_t
        else:
            player_body.velocity[0] = -.3
    elif player_body.grounded:
        go.switch_animation("idle")
        player_body.velocity[0] = player_body.velocity[0] * 0.07 * d_t
        if abs(player_body.velocity[0]) < 0.0001:
            player_body.velocity[0] = 0
    if abs(player_body.velocity[0]) > 1 and player_body.grounded:
            player_body.velocity[0] = 0
    
    #g_screen_surface.draw_rect(player_body.hitbox, (255,0,0))
    go.update(g_screen_surface, d_t, player_body.hitbox, (player_body.impact or not player_body.grounded))

    box = player_body.hitbox.copy()
    box.x += box.width / 3
    box.width = box.width / 3
    hitlist = box.collidelistall(traps)
    if(len(hitlist) and go.go.invisible == False):
        go.go.gib(g_particles, [player_body.hitbox.x - 200, player_body.hitbox.y -150], player_body.velocity)
    
    if (not go.go.invisible):
        g_screen_surface.target(player_body.hitbox.center)
    else:
        death_stamp += d_t
        g_zoom = vector_math.lerp(1.0, 1.001, death_stamp, 10.0)
        g_speed = vector_math.lerp(1.0, 1.05, death_stamp, 100.0)

    newsurf = pg.transform.scale(g_screen_surface.surface, [g_window.get_size()[0] * g_zoom, g_window.get_size()[1]* g_zoom])
    g_window.blit(newsurf, (0,0))

    if (go.go.invisible):
        g_window.blit(death_label, (200,200))

    if not go.go.invisible:
        for spot in leak_spots:
            pos = go.get_child_pos(spot, player_body.hitbox)
            rot = go.get_child(spot).global_rotation
            sign = 1
            if go.flip:
                sign = -1
                dif = 2 * (player_body.hitbox.centerx - pos[0])
                pos[0] += dif
            vel = [math.cos(rot) * sign, math.sin(rot)]
            g_particles.append(particle.Blood(pos, vel))

    pg.display.flip()
        