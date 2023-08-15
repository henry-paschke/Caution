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
ANIMATIONS_DIR = "animations/"

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE, pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED | pg.RESIZABLE)
g_clock = pg.time.Clock()
g_debug_font = pg.font.Font(None, 20)
g_json_filepath = ANIMATIONS_DIR + "run.anim"

ARM_LENGTH = 60
LEG_LENGTH = 70
img = pg.image.load("arm.png").convert_alpha()
arm = pg.transform.scale(img, (ARM_LENGTH * 2, ARM_LENGTH * 2))
leg = pg.transform.scale(img, (LEG_LENGTH * 2, LEG_LENGTH * 2))
body = pg.transform.scale(img, (240,360))
head = pg.transform.scale(img, (75,300))

image_list = [None, [[body, [[arm, [[arm, []]]], [arm, [[arm, []]]], [leg, [[leg, []]]], [leg, [[leg, []]]], [head, []]]]]]

go = game_object.create_game_object_from_file("skeletons/human.ske", image_list)
keyframes = utility.read_from_json(g_json_filepath)
go.read_serialized_data(keyframes[0])
animation = keyframe_animation.Keyframe_animation(go, keyframes, 500)

gos = []
animations = []
for i in range(15):
    gos.append(game_object.create_game_object_from_file("skeletons/human.ske", image_list))
    go.read_serialized_data(keyframes[0])
    animations.append(keyframe_animation.Keyframe_animation(gos[i], keyframes, random.randint(200, 700)))
    gos[i].local_position = [random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])]


while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()


    go.update(g_screen_surface, g_clock.get_rawtime())
    for g in gos:
        g.update(g_screen_surface, g_clock.get_rawtime())

    utility.stamp_text([str(g_clock.get_fps())], g_screen_surface, (20,20))
    animation.update(g_clock.get_rawtime())
    for a in animations:
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
        