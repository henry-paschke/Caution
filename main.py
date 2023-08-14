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

go = game_object.Game_object((500, 250), math.pi  / 6, 100, 3)
go.add_child(game_object.Game_object([0,0], -math.pi / 6, 100, 3))


while g_running:
    g_screen_surface.fill(BLACK)
    g_clock.tick()

    for i in range(1000):
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
        