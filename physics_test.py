import pygame as pg
import physics

BLUE = (0, 255, 0 )
pg.init()
screen = pg.display.set_mode((1000, 500))
pg.display.set_caption("Beeps.com (OMG!!!!!!!!)")
test = physics.Physics_object(50,20,200,200, 2)

clock = pg.time.Clock()
floor = pg.rect.Rect(0, 400, 1000, 10)


playing = True
while playing:
    d_time = clock.tick_busy_loop()
    screen.fill((0, 0, 0))
    test.draw(screen)
    test.update(d_time)
    test.collide_with_objects([floor], d_time)
    pg.draw.rect(screen, BLUE, floor)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                pg.quit()
                quit()

    pg.display.flip()
