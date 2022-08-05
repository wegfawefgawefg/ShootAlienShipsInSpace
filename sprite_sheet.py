import math

import pygame


class SpriteSheet:
    def __init__(self, path, width, height, sprite_width, sprite_height):
        self.path = path
        self.sheet = pygame.image.load(path)  # .convert_alpha()
        self.width, self.height, self.sprite_width, self.sprite_height = width, height, sprite_width, sprite_height
        self.half_sprite_width = sprite_width // 2
        self.half_sprite_height = sprite_height // 2

    def get_tile_area(self, i):
        y = math.floor(i / self.width)
        py = y * self.sprite_height
        x = i % self.width
        px = x * self.sprite_width
        return (px, py, self.sprite_width, self.sprite_height)

    def __repr__(self) -> str:
        return self.path


def draw_sprite(surface, sprite_sheet, tile, x, y):
    x, y = int(x), int(y)
    tile = tile % (sprite_sheet.width * sprite_sheet.height)
    surface.blit(
        sprite_sheet.sheet,
        (
            x - sprite_sheet.half_sprite_width,
            y - sprite_sheet.half_sprite_height
        ),
        sprite_sheet.get_tile_area(tile))
