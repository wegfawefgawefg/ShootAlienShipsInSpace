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

        self.physics = pymunk.Space()

        self.ship = Ship(self)
        self.star_field = StarField(self)

        self.ship_controller = ShipController(self, self.ship)
        self.bullet_controller = BulletController(self, self.ship)
        self.warp_controller = WarpController(self, self.star_field)
        self.controllers = [
            self.ship_controller,
            self.bullet_controller,
            self.warp_controller,
        ]

        self.bullets = []
        self.enemies = []
        self.enemies.append(Debris(self))
        self.enemies.append(Debris(self))
        self.enemies.append(Debris(self))
        self.enemies.append(Debris(self))
        self.kill_zones = KillZones(self)

        for song in self.game.music.space_battle_songs:
            song.play(loops=-1)

    def control(self, event):
        if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
            for song in self.game.music.space_battle_songs:
                song.stop()
            self.game.set_scene(main_menu.MainMenu(self.game))
            return

        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            for controller in self.controllers:
                controller.control(event.key, press=(event.type == pygame.KEYDOWN))

    def step(self):
        m = self.game.get_mouse_position()
        # TODO: you removed DT from the step args. you gotta go into each and make them pull from game object
        for controller in self.controllers:
            controller.step()
        self.physics.step(self.game.dt)
        self.star_field.step()
        for bullet in self.bullets:
            bullet.step()
        for enemy in self.enemies:
            enemy.step()
        self.kill_zones.step()
        self.ship.step()

    def draw(self):
        self.star_field.draw()
        for bullet in self.bullets:
            bullet.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.kill_zones.draw()
        self.ship.draw()

    def check_keyholding(self):
        """
        TODO:
        make general code for held buttons rather than pressed
        maybe holding is a bad mechanism in general?
        """
        # if name not in presstimes:
        #     continue
        # d = t - presstimes[name]
        # del presstimes[name]

        # # if d < PRESS_THRESHOLD:
        # #     print(f"{name} - pressed")
        # # else:
        # #     print(f"{name} - released after - {d}s")
