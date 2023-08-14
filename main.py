import pygame as pg
import game_object

#constants
SCREEN_SIZE = (960, 540)
BLACK  = (0,0,0)

g_running = True
g_screen_surface = pg.display.set_mode(SCREEN_SIZE)
g_game_objects = []

go = game_object.Game_object((500, 250), 3.141592653 / 4, 30, 33)


while g_running:
    g_screen_surface.fill(BLACK)

    go.chain_update(g_screen_surface)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            g_running = False
            pg.quit()
            quit()

    pg.display.flip()
        