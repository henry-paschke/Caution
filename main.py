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

go = game_object.Game_object((500, 250), math.pi / 6, 100, "parent")
go.add_child(game_object.Game_object([0,0], 0, 100, "child"))
go.seek_first_child("child").set_target(game_object.Target([100,0], 0, 2000))

print(go.get_visualization())

while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()
    g_elapsed += g_clock.get_rawtime()
    print(g_elapsed)

    go.local_rotation += g_clock.get_time() / 1000
    go.update(g_screen_surface, g_clock.get_rawtime() )

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

    pg.display.flip()
        