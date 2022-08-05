import pygame

import sprite_sheet


class SpriteSheets:
    def __init__(self) -> None:
        SHIP_SPRITES = sprite_sheet.SpriteSheet(
            "assets/ships.png", 10, 10, 8, 8)
        PARTICLE_SPRITES = sprite_sheet.SpriteSheet(
            "assets/particles.png", 6, 10, 8, 8)
