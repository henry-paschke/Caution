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
ANIMATIONS_DIR = "animations/"

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE)
g_clock = pg.time.Clock()
g_elapsed = 0
g_game_objects = []
g_playing = True
g_console_hidden = False
g_debug_font = pg.font.Font(None, 20)
g_frame_edit_number = 0
g_json_filepath = ANIMATIONS_DIR + "idle.anim"
g_clipboard = []
g_animating = True

ARM_LENGTH = 60
LEG_LENGTH = 70
img = pg.image.load("arm.png").convert_alpha()
arm = pg.transform.scale(img, (ARM_LENGTH * 2, ARM_LENGTH * 2))
leg = pg.transform.scale(img, (LEG_LENGTH * 2, LEG_LENGTH * 2))
body = pg.transform.scale(img, (240,360))
head = pg.transform.scale(img, (75,300))
go = game_object.Game_object([500, SCREEN_SIZE[1] - 30], 0, 100, "Base", None)
go.add_child(game_object.Game_object([0, -130], -math.pi / 2, 100, "Spine", body))
go.children[0].add_child(game_object.Game_object([0, -30], -math.pi / 2, ARM_LENGTH, "Left_arm_top", arm))
go.seek_first_child("Left_arm_top").add_child(game_object.Game_object([-ARM_LENGTH, 0], -math.pi / 4, ARM_LENGTH, "Left_arm_bottom", arm))
go.children[0].add_child(game_object.Game_object([-100, 30], math.pi / 8 * 5, ARM_LENGTH, "Right_arm_top", arm))
go.seek_first_child("Right_arm_top").add_child(game_object.Game_object([-ARM_LENGTH, 14], -math.pi / 4, ARM_LENGTH, "Right_arm_bottom", arm))
go.children[0].add_child(game_object.Game_object([0, -30], 3.9, LEG_LENGTH, "Left_leg_top", leg))
go.seek_first_child("Left_leg_top").add_child(game_object.Game_object([-LEG_LENGTH, 0], -math.pi / 3, LEG_LENGTH, "Left_leg_bottom", leg))
go.children[0].add_child(game_object.Game_object([0, 30], 2.5, LEG_LENGTH, "Right_leg_top", leg))
go.seek_first_child("Right_leg_top").add_child(game_object.Game_object([-LEG_LENGTH, 0], .3, LEG_LENGTH, "Right_leg_bottom", leg))
go.children[0].add_child(game_object.Game_object([-140, 0], 0, 30, "Head", head))

go.selected = True
g_selected = go

keyframes = utility.read_from_json(g_json_filepath)

go.read_serialized_data(keyframes[0])

animation = keyframe_animation.Keyframe_animation(go, keyframes, 500)

while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()
    g_elapsed += g_clock.get_rawtime()
    k = pg.key.get_pressed()


    go.update(g_screen_surface, g_clock.get_rawtime(), g_playing)

    if g_playing:
        animation.update(g_clock.get_rawtime())
    
    debug_str = ["filepath: " + g_json_filepath,
                 "FPS : " + str(g_clock.get_fps()),
                "Playing: " + str(g_playing), go.get_visualization(), "selected object: " + go.seek_selected().name, 
                  "< : select next sibling", "/\\ select first child", 
                 "\\/ select parent", "WASD : edit local position (alt to free move)", str(g_selected.local_position),
                  "QE : local rotation, ctrl to fine-tune", str(g_selected.local_rotation),
                  "frame number: " + str(animation.frame), "1 and []: override/change frame number " + str(g_frame_edit_number),
                  "2 : save current animation as " + g_json_filepath, "3 : save as new",
                  "4 : save this pose as a new frame", "frame count : " + str(len(keyframes))
                  ]
    utility.stamp_text(debug_str, g_screen_surface, (20,20))
    utility.stamp_text(g_console, g_screen_surface, (SCREEN_SIZE[0]- 260, 0))

    for e in pg.event.get():
        if e.type == pg.QUIT:
            g_running = False
            pg.quit()
            quit()
        if (e.type == pg.KEYDOWN):
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
                go.read_serialized_data(keyframes[g_frame_edit_number])
            if (e.key == pg.K_RIGHTBRACKET):
                g_frame_edit_number += 1
                if g_frame_edit_number >= len(animation.keyframe_list):
                    g_frame_edit_number = 0
                go.read_serialized_data(keyframes[g_frame_edit_number])
            if (e.key == pg.K_2):
                utility.save_to_json(g_json_filepath, keyframes)
            if (e.key == pg.K_3):
                print("type the name of the file:")
                g_json_filepath = ANIMATIONS_DIR + input() + ".anim"
                utility.save_to_json(g_json_filepath, keyframes)
            if (e.key == pg.K_l):
                print("type the name of the file:")
                g_json_filepath = ANIMATIONS_DIR + input() + ".anim"
                keyframes = utility.read_from_json(g_json_filepath)
                go.read_serialized_data(keyframes[0])
                animation = keyframe_animation.Keyframe_animation(go, keyframes, 500)
            if (e.key == pg.K_4):
                keyframes.append(go.serialize_data())
                animation.add_frame(go.serialize_data())
            if (e.key == pg.K_c):
                g_clipboard = go.serialize_data()
            if (e.key == pg.K_v):
                go.read_serialized_data(g_clipboard)
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
        