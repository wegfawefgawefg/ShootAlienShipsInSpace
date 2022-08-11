import pygame

import sprite_sheet


class SpriteSheets:
    def __init__(self) -> None:
        self.ships = sprite_sheet.SpriteSheet("assets/ships.png", 10, 10, 8, 8)
        self.particles = sprite_sheet.SpriteSheet("assets/particles.png", 6, 10, 8, 8)
