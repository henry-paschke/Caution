import pygame as pg
pg.init()

import game_object_editor
import math
import utility
from globals import *
import keyframe_animation
import vector_math
import copy

#constants
RES_SCALE = 1.5
SCREEN_SIZE = (960 * RES_SCALE, 540 * RES_SCALE)
BLACK  = (0,0,0)
WHITE = (255,255,255)
ANIMATIONS_DIR = "animations/"

g_running = True
g_window =  pg.display.set_mode(SCREEN_SIZE, pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
g_screen_surface = pg.surface.Surface(SCREEN_SIZE)
g_clock = pg.time.Clock()
g_elapsed = 0
g_game_objects = []
g_playing = True
g_console_hidden = False
g_debug_font = pg.font.Font(None, 20)
g_frame_edit_number = 0
g_json_filepath = ANIMATIONS_DIR + "idle.anim"
g_clipboard = []
g_assets = []

go = game_object_editor.create_game_object_from_file("skeletons/human.ske", g_assets)

g_selected = go
g_selected.select_first_child()

data = utility.read_from_json(g_json_filepath)
keyframes = data["frames"]
intervals = data["times"]

go.read_serialized_data(keyframes[0])

animation = keyframe_animation.Keyframe_animation(go, keyframes, intervals)


while g_running:
    g_screen_surface.fill(WHITE)
    g_clock.tick()
    g_elapsed += g_clock.get_rawtime()
    k = pg.key.get_pressed()
    kf = keyframes.copy()

    go.update(g_screen_surface, g_clock.get_rawtime(), g_playing)

    if g_playing:
        animation.update(g_clock.get_rawtime())

    frames_string = ''
    for i in range(len(keyframes)):
        if i == g_frame_edit_number:
            frames_string += ("{" + str(i) + "} ")
        else:
            frames_string += (" " + str(i) + "  ")
    
    debug_str = ["filepath: " + g_json_filepath,
                 "FPS : " + str(g_clock.get_fps()),
                "Playing: " + str(g_playing), go.get_visualization(), "selected object: " + go.seek_selected().name, 
                  "< : select next sibling", "/\\ select first child", 
                 "\\/ select parent", "WASD : edit local position (alt to free move)", str(g_selected.local_position),
                  "QE : local rotation, ctrl to fine-tune", str(g_selected.local_rotation),
                  "frame number: " + str(animation.frame), "1 and []: override/change frame number " + str(g_frame_edit_number),
                  "2 : save current animation as " + g_json_filepath, "3 : save as new",
                  "4 : save this pose as a new frame", "frame count : " + str(len(keyframes)),
                  str(keyframes), "Frame " + str(g_frame_edit_number) + " length in Ms : " + str(intervals[g_frame_edit_number]),
                  "comma/period : change length of frame", frames_string, "5 : duplicate left, 6 : duplicate right"
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
            if (e.key == pg.K_1): # this is the number one not the letter L
                data = copy.deepcopy(go.serialize_data())
                keyframes[g_frame_edit_number] = data
                animation.change_animation(g_frame_edit_number, data, intervals[g_frame_edit_number])
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
                console_log("Saved!")
                save_data = {
                    "frames" : keyframes,
                    "times" : intervals
                }
                utility.save_to_json(g_json_filepath, save_data)
            if (e.key == pg.K_3):
                print("type the name of the file:")
                g_json_filepath = ANIMATIONS_DIR + input() + ".anim"
                open(g_json_filepath, "x")
                utility.save_to_json(g_json_filepath, keyframes)
            if (e.key == pg.K_l): # this is the letter L not the number one
                print("type the name of the file:")
                g_json_filepath = ANIMATIONS_DIR + input() + ".anim"
                load_data = utility.read_from_json(g_json_filepath)
                keyframes = load_data["frames"]
                intervals = load_data["times"]
                go.read_serialized_data(keyframes[0])
                animation = keyframe_animation.Keyframe_animation(go, keyframes, intervals)
            if (e.key == pg.K_4):
                keyframes.append(go.serialize_data())
                intervals.append(intervals[g_frame_edit_number])
                animation.add_frame(go.serialize_data(), intervals[g_frame_edit_number])
            if (e.key == pg.K_5):
                keyframes.insert(g_frame_edit_number - 1, copy.deepcopy(keyframes[g_frame_edit_number]))
                intervals.insert(g_frame_edit_number - 1, intervals[g_frame_edit_number])
                animation.reset_keyframe_list(keyframes, intervals)
            if (e.key == pg.K_6):
                keyframes.insert(g_frame_edit_number, copy.deepcopy(keyframes[g_frame_edit_number]))
                intervals.insert(g_frame_edit_number, intervals[g_frame_edit_number])
                animation.reset_keyframe_list(keyframes, intervals)
            if (e.key == pg.K_c):
                g_clipboard = go.serialize_data()
            if (e.key == pg.K_v):
                go.read_serialized_data(g_clipboard)
            if (e.key == pg.K_COMMA):
                value = intervals[g_frame_edit_number] - 25
                if (intervals[g_frame_edit_number] < 25):
                    value = 25
                intervals[g_frame_edit_number] = value
                animation.change_animation(g_frame_edit_number, keyframes[g_frame_edit_number], value)

            if (e.key == pg.K_PERIOD):
                value = intervals[g_frame_edit_number] + 25
                intervals[g_frame_edit_number] = value
                animation.change_animation(g_frame_edit_number, keyframes[g_frame_edit_number], value)
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

    #pg.draw.circle(g_screen_surface, (255,0,0), vector_math.add_vector2(go.children[0].target.position, (250, 200)), 20)
    if (kf != keyframes):
        print("alert")

    #pg.draw.rect(g_screen_surface, (0,0, 255), (SCREEN_SIZE[0] / 2 - 5, (SCREEN_SIZE[1] - (SCREEN_SIZE[1] / 3)) - 5, 10, 10))
    g_window.blit(pg.transform.scale(g_screen_surface, pg.display.get_window_size()), (0, 0))
    pg.display.flip()
        