import pygame as pg
import game_object
import math

#constants
SCREEN_SIZE = (960, 540)
BLACK  = (0,0,0)

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE)
g_clock = pg.time.Clock()
g_elapsed = 0
g_game_objects = []

go = game_object.Game_object([500, 250], math.pi / 3, 100, "parent")
go.add_child(game_object.Game_object([0,250], -math.pi * 30, 100, "child"))
go.seek_first_child("child").add_child(game_object.Game_object([0,20], math.pi / 2, 100, "child_2"))
#go.seek_first_child("child").set_target(game_object.Target([100,0], math.pi, 2000))

print(go.get_visualization())
go.set_keyframe(game_object.create_keyframe_from_serialized([[500, 250], 1.4465987755982501, [[[46.150000000000006, 0.0], 1.4498450096316895, [[[0, 100], 1.5707963267948966, []]]]]], 1000))


while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()
    g_elapsed += g_clock.get_rawtime()

    #go.local_rotation += g_clock.get_time() / 1000
    go.update(g_screen_surface, g_clock.get_rawtime())


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
                print(go.target.position)

    pg.display.flip()
        