import pyglet as pg
import game_object
import utility
import keyframe_animation

RES_SCALE = 1
SCREEN_SIZE = (960 * RES_SCALE, 540 * RES_SCALE)
BLACK  = (0,0,0)
ANIMATIONS_DIR = "animations/"

g_window = pg.window.Window(SCREEN_SIZE[0], SCREEN_SIZE[1])

g_json_filepath = ANIMATIONS_DIR + "idle.anim"

ARM_LENGTH = 60
LEG_LENGTH = 70
img = pg.image.load("arm.png")
""" arm = pg.transform.scale(img, (ARM_LENGTH * 2, ARM_LENGTH * 2))
leg = pg.transform.scale(img, (LEG_LENGTH * 2, LEG_LENGTH * 2))
body = pg.transform.scale(img, (240,360))
head = pg.transform.scale(img, (75,300)) """


@g_window.event
def on_draw():
    g_window.clear()

def update(dt):
    print(dt)
    

pg.clock.schedule_interval(update, 1/120.0)

pg.app.run()