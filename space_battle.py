import pygame
from pygame.locals import (
    K_q,
    K_ESCAPE,
)
import pymunk

from scene import Scene
from ship import Ship
from starfield import StarField
from ship_controller import ShipController
from bullet_controller import BulletController
from warp_controller import WarpController
from debris import Debris
from killzones import KillZones
import main_menu

class SpaceBattle(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.create_physics()

        self.ship = Ship(self)
        self.star_field = StarField(self)
        for _ in range(0, 4):
            Debris(self)
        KillZones(self)

        self.ship_controller = ShipController(self, self.ship)
        self.bullet_controller = BulletController(self, self.ship)
        self.warp_controller = WarpController(self, self.star_field)

        for song in self.game.music.space_battle_songs:
            song.play(loops=-1)

    def control(self, event):
        if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
            for song in self.game.music.space_battle_songs:
                song.stop()
            self.game.set_scene(main_menu.MainMenu(self.game))
            return
        super().control(event)

    def check_keyholding(self):
        """
        TODO:
        make general code for held buttons rather than pressed
        maybe holding is a bad mechanism in general?
        """
        pass
        # if name not in presstimes:
        #     continue
        # d = t - presstimes[name]
        # del presstimes[name]

        # # if d < PRESS_THRESHOLD:
        # #     print(f"{name} - pressed")
        # # else:
        # #     print(f"{name} - released after - {d}s")
