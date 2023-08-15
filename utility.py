import pygame as pg
import json
 
g_debug_font = pg.font.Font(None, 16)

def stamp_text(lines, surf, pos):
    for i in range(len(lines)):
        text_surface = g_debug_font.render(lines[i], True, (255,255,255))
        surf.blit(text_surface, (pos[0], pos[1] + 20 * i))

def read_from_json(s):
    with open(s, "r") as f:
        return json.load(f)
    
def save_to_json(s, serialized_data):
    with open(s, "w") as f:
        return json.dump(serialized_data, f)