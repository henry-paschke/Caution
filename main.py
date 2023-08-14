import pygame as pg
import game_object
import math

#constants
SCREEN_SIZE = (960, 540)
BLACK  = (0,0,0)

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE)
g_clock = pg.time.Clock()
g_game_objects = []

go = game_object.Game_object((500, 250), math.pi  / 6, 100, "parent")
go.add_child(game_object.Game_object([120,0], -math.pi / 6, 100, "child"))

print(go.get_visualization())

while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()

    go.local_rotation += g_clock.get_time() / 1000
    go.update(g_screen_surface)

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
        