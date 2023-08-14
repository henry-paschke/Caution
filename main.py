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
g_frame_edit_number = 0

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
go.read_serialized_data([[557.5, 499], 0, [[[10.0, -130], 4.71238898038469, [[[-100, -30], 4.71238898038469, [[[-60, 0], 5.497787143782138, []]]], [[-99, 30], 1.7934954084936243, [[[-60, 0], 5.497787143782138, []]]], [[0, -30], 3.9, [[[-70, 0], 5.497787143782138, []]]], [[0, 30], 2.5, [[[-70, 0], 0.3, []]]], [[-140, 0], 0, []]]]]])

keyframes = [
    [[557.5, 499], 0, [[[10.0, -130], 4.71238898038469, [[[-100, -30], 4.71238898038469, [[[-60, 0], 5.497787143782138, []]]], [[-99, 30], 1.7934954084936243, [[[-60, 0], 5.497787143782138, []]]], [[0, -30], 3.9, [[[-70, 0], 5.497787143782138, []]]], [[0, 30], 2.5, [[[-70, 0], 0.3, []]]], [[-140, 0], 0, []]]]]],
    [[557.5, 499], 0, [[[10.0, -130], 4.7498889803846955, [[[-100, -30], 4.249888980384617, [[[-60, 0], 5.420287143782126, []]]], [[-99, 30], 3.0859954084935968, [[[-60, 0], 5.497787143782138, []]]], [[0, -30], 2.917500000000021, [[[-70, 0], 1.269601836602659, []]]], [[0, 30], 1.7175000000000167, [[[-70, 0], 0.3, []]]], [[-140, 0], 0, []]]]]],
]


#dab
#keyframes = [[[557.5, 499.0], 0.0, [[[10.0, -130.0], 4.720563980384691, [[[-100.0, -30.0], 5.706563980384845, [[[-60.0, 0.0], 5.480892143782135, []]]], [[-99.0, 30.0], 0.8302604084936451, [[[-60.0, 0.0], 5.497787143782138, []]]], [[0.0, -30.0], 4.700815000000107, [[[-70.0, 0.0], 5.945777143782161, []]]], [[0.0, 30.0], 0.9794150000000323, [[[-70.0, 0.0], 0.3, []]]], [[-140.0, 0.0], 0.0, []]]]]], [[557.5, 499.0], 0, [[[10.0, -130.0], 4.7498889803846955, [[[-100.0, -30.0], 4.249888980384617, [[[-60.0, 0.0], 5.420287143782126, []]]], [[-99.0, 30.0], 3.0859954084935968, [[[-60.0, 0.0], 5.497787143782138, []]]], [[0.0, -30.0], 2.917500000000021, [[[-70.0, 0.0], 1.269601836602659, []]]], [[0.0, 30.0], 2.509499999999983, [[[-70.0, 0.0], 0.7464999999999987, []]]], [[-140.0, 0.0], 0, []]]]]]]
#jumping jacks
keyframes = [[[557.5, 499.0], 0, [[[0.0, -136.27200000000002], 4.71238898038469, [[[-100.0, -30.0], 3.5773889803845877, [[[-60.0, 0.0], 6.207787143782247, []]]], [[-99.0, 30.0], 2.9009954084936007, [[[-60.0, 0.0], 6.260287143782257, []]]], [[0.0, -30.0], 3.230000000000012, [[[-70.0, 0.0], 0.02960183660261176, []]]], [[0.0, 30.0], 2.98749999999999, [[[-70.0, 0.0], 0.10249999999999863, []]]], [[-140.0, 0.0], 0, []]]]]], [[557.5, 499.0], 0, [[[0.0, -131.008], 4.71238898038469, [[[-100.0, -30.0], 5.459888980384805, [[[-60.0, 0.0], 6.207787143782247, []]]], [[-99.0, 30.0], 0.9059954084936432, [[[-60.0, 0.0], 6.260287143782257, []]]], [[0.0, -30.0], 3.6350000000000033, [[[-70.0, 0.0], 0.02960183660261176, []]]], [[0.0, 30.0], 2.5824999999999987, [[[-70.0, 0.0], 0.10249999999999863, []]]], [[-140.0, 0.0], 0, []]]]]]]

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
                  "frame number: " + str(animation.frame), "1 and []: override/change frame number " + str(g_frame_edit_number),
                  "2 : print current animation as serialized data", "3 : snap to frame number " + str(g_frame_edit_number)
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
            if (e.key == pg.K_SPACE):
                g_playing = not g_playing
            if (e.key == pg.K_1):
                animation.change_animation(g_frame_edit_number, go.serialize_data())
                keyframes[g_frame_edit_number] = go.serialize_data()
                console_log("changed frame " + str(g_frame_edit_number) + " to current pose")
            if (e.key == pg.K_LEFTBRACKET):
                g_frame_edit_number -= 1
                if g_frame_edit_number < 0:
                    g_frame_edit_number = len(animation.keyframe_list) - 1
            if (e.key == pg.K_RIGHTBRACKET):
                g_frame_edit_number += 1
                if g_frame_edit_number >= len(animation.keyframe_list):
                    g_frame_edit_number = 0
            if (e.key == pg.K_2):
                print(keyframes)
            if (e.key == pg.K_3):
                go.read_serialized_data(keyframes[g_frame_edit_number])
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
        