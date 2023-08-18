import pygame as pg
import physics

BLUE = (0, 255, 0 )
pg.init()
screen = pg.display.set_mode((1000, 500))
pg.display.set_caption("Beeps.com (OMG!!!!!!!!)")
test = physics.Physics_object(50,20,20,20,5)

clock = pg.time.Clock()
floors = [
    pg.rect.Rect(0, 400, 1000, 10),
    pg.rect.Rect(900, 0, 30, 1000)
]


playing = True
while playing:
    d_time = clock.tick_busy_loop(120)
    screen.fill((0, 0, 0))
    test.draw(screen)
    test.update(d_time)
    test.collide_with_objects(floors, d_time)
    for f in floors:
        pg.draw.rect(screen, BLUE, f)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                pg.quit()
                quit()
            if e.key == pg.K_SPACE:
                test.velocity[1] = -1
                test.grounded = False

    k = pg.key.get_pressed()
    if (k[pg.K_d] and test.grounded):
        if test.velocity[0] > 0:
            test.velocity[0] = test.velocity[0] + 0.0007 * d_time
        else:
            test.velocity[0] = .3
    elif (k[pg.K_a] and test.grounded):
        if test.velocity[0] < 0:
            test.velocity[0] = test.velocity[0] - 0.0007 * d_time
        else:
            test.velocity[0] = -.3
    elif test.grounded:
        test.velocity[0] = test.velocity[0] * 0.07 * d_time

    

    pg.display.flip()
