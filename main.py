import pygame as pg
pg.init()

import game_object
import utility
import keyframe_animation
import random

#python -m cProfile -o main.prof main.py   
#python -m snakeviz main.prof -b windows-default

#constants
RES_SCALE = 2
SCREEN_SIZE = (960 * RES_SCALE, 540 * RES_SCALE)
BLACK  = (0,0,0)
WHITE = (255,255,255)
ANIMATIONS_DIR = "animations/"

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE, pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED | pg.RESIZABLE)
g_clock = pg.time.Clock()
g_debug_font = pg.font.Font(None, 20)
g_json_filepath = ANIMATIONS_DIR + "idle.anim"

g_assets = []

go = game_object.create_game_object_from_file("skeletons/human.ske", g_assets)
animation = keyframe_animation.create_animation("animations/slip.anim", go)

gos = []
ans = []
for i in range(0):
    gos.append(game_object.create_game_object_from_file("skeletons/human.ske", g_assets))
    ans.append(keyframe_animation.create_animation("animations/slip.anim", gos[i]))
    gos[i].local_position = (random.randint(0, 1920), random.randint(0, 1080))


while g_running:
    g_screen_surface.fill(WHITE)
    g_clock.tick()

    go.update(g_screen_surface, g_clock.get_rawtime())
    for g in gos:
        g.update(g_screen_surface, g_clock.get_rawtime())
    utility.stamp_text([str(g_clock.get_fps())], g_screen_surface, (20,20))
    animation.update(g_clock.get_rawtime())
    for a in ans:
        a.update(g_clock.get_rawtime())

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

    pg.display.flip()
        