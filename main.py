import pygame as pg
pg.init()

import game_object
import utility
import keyframe_animation
import random
import animation_wrapper
import physics

#python -m cProfile -o main.prof main.py   
#python -m snakeviz main.prof -b windows-default

#constants
RES_SCALE = 2
SCREEN_SIZE = (960 * RES_SCALE, 540 * RES_SCALE)
BLACK  = (0,0,0)
WHITE = (255,255,255)

g_running = True
g_screen_surface = pg.surface.Surface(SCREEN_SIZE)
g_window = pg.display.set_mode((960, 540), pg.SCALED | pg.RESIZABLE)
g_clock = pg.time.Clock()
g_debug_font = pg.font.Font(None, 20)

g_assets = []

go = animation_wrapper.Animation_wrapper("skeletons/human.ske", "tumble", g_assets, ["walk", "idle", "jump"])

player_body = physics.Physics_object(0,0,300,350, 4)

floors = [
    pg.rect.Rect(0, 900, 2000, 500),
    pg.rect.Rect(1500, 0, 500, 1000)
]


while g_running:
    g_screen_surface.fill(WHITE)
    d_t = g_clock.tick_busy_loop(120)

    player_body.draw(g_screen_surface)
    
    utility.stamp_text([str(g_clock.get_fps())], g_screen_surface, (20,20))

    player_body.update(d_t)
    player_body.collide_with_objects(floors, d_t)
    for f in floors:
        pg.draw.rect(g_screen_surface, (0,0,0), f)

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
            if e.key == pg.K_SPACE:
                player_body.velocity[1] = -1
                player_body.grounded = False
                player_body.impact = False
                go.switch_animation("jump")

    if (player_body.impact and player_body.grounded == False):
        go.switch_animation("tumble")    

    k = pg.key.get_pressed()
    if (k[pg.K_d]):
        if player_body.grounded:
            go.switch_animation("walk")
            go.flip = False
        if player_body.velocity[0] > 0:
            player_body.velocity[0] = player_body.velocity[0] + 0.0007 * d_t
        else:
            player_body.velocity[0] = .3
    elif (k[pg.K_a]):
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
    
    go.update(g_screen_surface, d_t, [player_body.hitbox.x - 100, player_body.hitbox.y -150])
    g_window.blit(pg.transform.scale(g_screen_surface, g_window.get_size(), g_window), (0,0))
    pg.display.flip()
        