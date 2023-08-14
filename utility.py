import pygame as pg

g_debug_font = pg.font.Font(None, 16)

def stamp_text(lines, surf, pos):
    for i in range(len(lines)):
        text_surface = g_debug_font.render(lines[i], True, (255,255,255))
        surf.blit(text_surface, (pos[0], pos[1] + 20 * i))
