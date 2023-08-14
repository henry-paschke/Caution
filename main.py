import pygame as pg
pg.init()

import game_object
import math
import utility
from globals import *

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


go = game_object.Game_object([500, 250], math.pi / 70, 100, "parent")
go.add_child(game_object.Game_object([0,250], -math.pi * 15, 100, "child"))
go.seek_first_child("child").add_child(game_object.Game_object([0,2000], math.pi / 2, 100, "child_2"))
go.seek_first_child("child").add_child(game_object.Game_object([0,2000], math.pi / 4, 100, "child_3"))
go.seek_first_child("child_2").selected = True
g_selected = go.seek_first_child("child_2")

go.set_keyframe(game_object.create_keyframe_from_serialized([[500, 250], 1.4465987755982501, [[[46.150000000000006, 0.0], 1.4498450096316895, [[[0, 100], 1.5707963267948966, []], [[0, 100], 1.5707963267948966 * 2, []]]]]], 1000))


while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()
    g_elapsed += g_clock.get_rawtime()

    #go.local_rotation += g_clock.get_time() / 1000
    if (g_playing):
        go.update(g_screen_surface, g_clock.get_rawtime())
    else:
        go.draw_recursive()
    
    debug_str = ["Playing: " + str(g_playing), go.get_visualization(), "selected object: " + go.seek_selected().name, "9 : print serialized data", "< : select next sibling", "/\\ select first child", "\\/ select parent"]
    utility.stamp_text(debug_str, g_screen_surface, (20,20))
    utility.stamp_text(g_console, g_screen_surface, (SCREEN_SIZE[0]- 260, 0))

    for e in pg.event.get():
        if e.type == pg.QUIT:
            g_running = False
            pg.quit()
            quit()
        if (e.type == pg.KEYDOWN):
            if (e.key == pg.K_a):
                go.local_rotation -= math.pi / 24
            if (e.key == pg.K_d):
                go.local_rotation += math.pi / 24
            if (e.key == pg.K_0):
                go.read_serialized_data([[500, 250], 1.4465987755982501, [[[46.150000000000006, 0.0], 1.4498450096316895, [[[0, 100], 1.5707963267948966, []]]]]])
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
            if (e.key == pg.K_BACKSLASH):
                g_console.pop(0)
                if pg.key.get_pressed()[pg.K_LCTRL]:
                    g_console.clear()

    pg.display.flip()
        