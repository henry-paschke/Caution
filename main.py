import pygame as pg
pg.init()

import game_object
import math
import utility
from globals import *
import keyframe_animation

pg.init()

#constants
SCREEN_SIZE = (960, 540)
BLACK  = (0,0,0)

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE)
g_clock = pg.time.Clock()
g_elapsed = 0
g_game_objects = []
g_playing = True
g_console_hidden = False
g_debug_font = pg.font.Font(None, 20)

g_animating = True

ARM_LENGTH = 60
LEG_LENGTH = 70

go = game_object.Game_object([500, SCREEN_SIZE[1] - 30], 0, 100, "Base")
go.add_child(game_object.Game_object([0, -130], -math.pi / 2, 100, "Spine"))
go.children[0].add_child(game_object.Game_object([0, -30], -math.pi / 2, ARM_LENGTH, "Left_arm_top"))
go.seek_first_child("Left_arm_top").add_child(game_object.Game_object([-ARM_LENGTH, 0], -math.pi / 4, ARM_LENGTH, "Left_arm_bottom"))
go.children[0].add_child(game_object.Game_object([-100, 30], math.pi / 8 * 5, ARM_LENGTH, "Right_arm_top"))
go.seek_first_child("Right_arm_top").add_child(game_object.Game_object([-ARM_LENGTH, 14], -math.pi / 4, ARM_LENGTH, "Right_arm_bottom"))
go.children[0].add_child(game_object.Game_object([0, -30], 3.9, LEG_LENGTH, "Left_leg_top"))
go.seek_first_child("Left_leg_top").add_child(game_object.Game_object([-LEG_LENGTH, 0], -math.pi / 3, LEG_LENGTH, "Left_leg_bottom"))
go.children[0].add_child(game_object.Game_object([0, 30], 2.5, LEG_LENGTH, "Right_leg_top"))
go.seek_first_child("Right_leg_top").add_child(game_object.Game_object([-LEG_LENGTH, 0], .3, LEG_LENGTH, "Right_leg_bottom"))
go.children[0].add_child(game_object.Game_object([-140, 0], 0, 30, "Head"))

go.selected = True
g_selected = go

keyframes = [
    [[557.5, 499], 0, [[[10.0, -130], 4.71238898038469, [[[-100, -30], 4.71238898038469, [[[-60, 0], 5.497787143782138, []]]], [[-99, 30], 1.7934954084936243, [[[-60, 0], 5.497787143782138, []]]], [[0, -30], 3.9, [[[-70, 0], 5.497787143782138, []]]], [[0, 30], 2.5, [[[-70, 0], 0.3, []]]], [[-140, 0], 0, []]]]]],
    [[557.5, 499], 0, [[[10.0, -130], 4.7498889803846955, [[[-100, -30], 4.249888980384617, [[[-60, 0], 5.420287143782126, []]]], [[-99, 30], 3.0859954084935968, [[[-60, 0], 5.497787143782138, []]]], [[0, -30], 2.917500000000021, [[[-70, 0], 1.269601836602659, []]]], [[0, 30], 1.7175000000000167, [[[-70, 0], 0.3, []]]], [[-140, 0], 0, []]]]]],
]

animation = keyframe_animation.Keyframe_animation(go, keyframes, 500)


while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()
    g_elapsed += g_clock.get_rawtime()
    k = pg.key.get_pressed()

    #go.local_rotation += g_clock.get_time() / 1000

    go.update(g_screen_surface, g_clock.get_rawtime(), g_playing)

    if g_playing:
        animation.update(g_clock.get_rawtime())
    
    debug_str = ["Playing: " + str(g_playing), go.get_visualization(), "selected object: " + go.seek_selected().name, 
                 "9 : print serialized data", "< : select next sibling", "/\\ select first child", 
                 "\\/ select parent", "WASD : edit local position (alt to free move)", str(g_selected.local_position),
                  "QE : local rotation, ctrl to fine-tune", str(g_selected.local_rotation),
                  "frame number: " + str(animation.frame)
                  ]
    utility.stamp_text(debug_str, g_screen_surface, (20,20))
    utility.stamp_text(g_console, g_screen_surface, (SCREEN_SIZE[0]- 260, 0))

    for e in pg.event.get():
        if e.type == pg.QUIT:
            g_running = False
            pg.quit()
            quit()
        if (e.type == pg.KEYDOWN):
            if (e.key == pg.K_0):
                #go.read_serialized_data()
                pass
            if (e.key == pg.K_9):
                print(go.serialize_data())
            if (e.key == pg.K_LEFT):
                g_selected = g_selected.select_sibling()
            if (e.key == pg.K_DOWN):
                g_selected = g_selected.select_parent()   
            if (e.key == pg.K_UP): 
                g_selected = g_selected.select_first_child()  
                print(g_selected) 
            if (e.key == pg.K_SPACE):
                g_playing = not g_playing
            if (e.key == pg.K_1):
                pass
            if (not k[pg.K_LSHIFT]):
                if (e.key == pg.K_d):
                    g_selected.local_position[0] += 1
                    if pg.key.get_pressed()[pg.K_LCTRL]:
                        g_selected.local_position[0] += 10
                if (e.key == pg.K_a):
                    g_selected.local_position[0] -= 1
                    if pg.key.get_pressed()[pg.K_LCTRL]:
                        g_selected.local_position[0] -= 10
                if (e.key == pg.K_w):
                    g_selected.local_position[1] -= 1
                    if pg.key.get_pressed()[pg.K_LCTRL]:
                        g_selected.local_position[1] -= 10
                if (e.key == pg.K_s):
                    g_selected.local_position[1] += 1
                    if pg.key.get_pressed()[pg.K_LCTRL]:
                        g_selected.local_position[1] += 10

            if (e.key == pg.K_BACKSLASH):
                g_console.pop(0)
                if pg.key.get_pressed()[pg.K_LCTRL]:
                    g_console.clear()
    
    if (k[pg.K_LALT]):
        if k[pg.K_d]:
            if k[pg.K_LCTRL]:
                g_selected.local_position[0] += g_clock.get_rawtime() / 20
            else:
                g_selected.local_position[0] += 1 * g_clock.get_rawtime() /2
        if k[pg.K_a]:
            if k[pg.K_LCTRL]:
                g_selected.local_position[0] -= g_clock.get_rawtime() / 20
            else:
                g_selected.local_position[0] -= 1 * g_clock.get_rawtime() /2
        if k[pg.K_w]:
            if k[pg.K_LCTRL]:
                g_selected.local_position[1] -= g_clock.get_rawtime() / 20
            else:
                g_selected.local_position[1] -= 1 * g_clock.get_rawtime() /2
        if k[pg.K_s]:
            if k[pg.K_LCTRL]:
                g_selected.local_position[1] += g_clock.get_rawtime() / 20
            else:
                g_selected.local_position[1] += g_clock.get_rawtime() /2
    if k[pg.K_q]:
        if k[pg.K_LCTRL]:
            g_selected.local_rotation -= g_clock.get_rawtime() / 1000
        else:
            g_selected.local_rotation -= 1 * g_clock.get_rawtime() /400
    if k[pg.K_e]:
        if k[pg.K_LCTRL]:
            g_selected.local_rotation += g_clock.get_rawtime() / 1000
        else:
            g_selected.local_rotation += g_clock.get_rawtime() /400

    pg.display.flip()
        