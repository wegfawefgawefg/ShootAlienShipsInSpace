import math
from pprint import pprint
import random

import math
from types import new_class
import pygame
from pygame import K_SPACE, Vector2
from pygame.locals import (
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_LEFT, K_RIGHT, K_UP, K_DOWN,
    K_a, K_s, K_d, K_f,
)

PRESS_THRESHOLD = 100


SCREEN_DIMS = Vector2(240, 160)
WINDOW_DIMS = SCREEN_DIMS * 4.0

PRIMARY_SURFACE = None
WINDOW = None

SHIP_SPRITES = None
PARTICLE_SPRITES = None

LASER_SOUNDS = None
WARP_SOUNDS = None
MUSIC = None

MOUSE_POSITION = None

BULLETS = []


class StarField:
    def __init__(self):
        self.warp_level = 0.0
        self.stars = []
        for _ in range(200):
            y = random.random() * SCREEN_DIMS.y * 2.0 - SCREEN_DIMS.y // 2
            self.new_star(y)

    def new_star(self, y=None):
        center_x = SCREEN_DIMS.x / 2.0
        y = y if y else -(SCREEN_DIMS.y // 2)
        p = Vector2(SCREEN_DIMS.x * random.random() * 2.0, y)
        p.x -= SCREEN_DIMS.x // 2.0
        vy = (20.0 + (abs((center_x - p.x)) * 0.08) ** 2.0)
        v = Vector2(0.0, vy)
        new_star = Star(p, v)
        self.stars.append(new_star)

    def step(self, dt):
        if random.random() > 0.5:
            self.new_star()

        for star in self.stars:
            star.step(dt * (1.0 + self.warp_level))
            if star.pos.y >= (SCREEN_DIMS.y * 1.5):
                self.kill(star)

    def kill(self, star):
        for i in range(len(self.stars)):
            s = self.stars[i]
            if star.id == s.id:
                self.stars.pop(i)
                break

    def draw(self, ship):
        c = SCREEN_DIMS / 2.0
        for star in self.stars:
            offset = (c.elementwise() - ship.pos) / 2
            star.draw(offset)


class Star:
    ID = 0

    def __init__(self, pos, vel):
        self.id = Star.ID
        Star.ID += 1
        self.pos = Vector2(pos.x, pos.y)
        self.vel = Vector2(vel.x, vel.y)

    def step(self, dt):
        self.pos += self.vel * dt

    def draw(self, offset):
        p = offset + self.pos
        PARTICLE_SPRITES.draw_sprite(28, p.x, p.y)


class SpriteSheet:
    def __init__(self, path, width, height, sprite_width, sprite_height):
        self.path = path
        self.sheet = pygame.image.load(path)  # .convert_alpha()
        self.width, self.height, self.sprite_width, self.sprite_height = width, height, sprite_width, sprite_height
        self.half_sprite_width = sprite_width // 2
        self.half_sprite_height = sprite_height // 2

    def draw_sprite(self, tile, x, y):
        x, y = int(x), int(y)
        tile = tile % (self.width * self.height)
        PRIMARY_SURFACE.blit(self.sheet, (x - self.half_sprite_width, y -
                                          self.half_sprite_height), self.get_tile_area(tile))

    def get_tile_area(self, i):
        y = math.floor(i / self.width)
        py = y * self.sprite_height
        x = i % self.width
        px = x * self.sprite_width
        return (px, py, self.sprite_width, self.sprite_height)

    def __repr__(self) -> str:
        return self.path


class Bullet:
    ID = 0
    MIN_SPEED = 0.1
    SPEED_PER_TYPE = 0.2
    MAX_TYPE = 11
    MIN_LIFE = 0.02
    LIFE_SPAN_PER_TYPE = 0.04

    def __init__(self, pos, t) -> None:
        self.age = 0
        self.creation_time = pygame.time.get_ticks()
        self.id = Bullet.ID
        Bullet.ID += 1

        self.moving = False
        self.pos = pos
        self.pos.y - 8
        self.t = t
        BULLETS.append(self)

    def step(self, dt):
        if self.moving:
            self.age += dt
            self.pos.y -= Bullet.MIN_SPEED + Bullet.SPEED_PER_TYPE * self.t

        if self.age > (Bullet.MIN_LIFE + Bullet.LIFE_SPAN_PER_TYPE * self.t):
            self.kill()
        if self.pos.y < 0:
            self.kill()

    def kill(self):
        for i in range(len(BULLETS)):
            bullet = BULLETS[i]
            if bullet.id == self.id:
                BULLETS.pop(i)
                break

    def charge(self, t):
        self.t = min(Bullet.MAX_TYPE, (t - self.creation_time) // 16)

    def release(self):
        self.moving = True

    def draw(self):
        PARTICLE_SPRITES.draw_sprite(self.t, self.pos.x, self.pos.y)


class Ship:
    def __init__(self):
        self.vel = Vector2(0.0, 0.0)
        self.pos = Vector2(SCREEN_DIMS.x//2, SCREEN_DIMS.y*0.8)

    def step(self, dt):
        self.pos += self.vel * dt
        self.vel *= 0.98

        if self.pos.y >= SCREEN_DIMS.y:
            self.pos.y = SCREEN_DIMS.y
            self.vel.y = 0.0

        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        elif self.pos.x > SCREEN_DIMS.x:
            self.pos.x = SCREEN_DIMS.x
            self.vel.x = 0

    def fly(self, dir):
        self.vel += dir * 2.0

    def draw(self):
        sprite = 1
        if self.vel.x <= -10:
            sprite = 0
        if self.vel.x >= 10:
            sprite = 2
        SHIP_SPRITES.draw_sprite(sprite, self.pos.x, self.pos.y)


class Controller:
    def __init__(self):
        pass

    def control(self, key, press):
        raise NotImplementedError

    def step(dt):
        raise NotImplementedError


class WarpController(Controller):
    def __init__(self, star_field):
        self.star_field = star_field
        self.warping = False

    def control(self, key, press):
        if key == K_SPACE:
            if press:
                self.warping = True
                WARP_SOUNDS[0].play()
            else:
                self.warping = False
                self.warp_level = 0.0
                WARP_SOUNDS[-1].play()

    def step(self, dt):
        if self.warping:
            self.star_field.warp_level += dt * 0.00001
            self.star_field.warp_level = min(20.0, self.star_field.warp_level)
            for _ in range(10):
                self.star_field.new_star()
        else:
            self.star_field.warp_level = max(
                self.star_field.warp_level*0.99,
                0.0)


class ShipController(Controller):
    def __init__(self, ship):
        self.ship = ship
        self.down = {
            K_LEFT: False,
            K_RIGHT: False,
            K_UP: False,
            K_DOWN: False
        }

    def control(self, key, press):
        self.down[key] = press

    def step(self, t):
        if self.down[K_LEFT]:
            self.ship.fly(Vector2(-1.0, 0.0))
        if self.down[K_RIGHT]:
            self.ship.fly(Vector2(1.0, 0.0))
        if self.down[K_UP]:
            self.ship.fly(Vector2(0.0, -1.0))
        if self.down[K_DOWN]:
            self.ship.fly(Vector2(0.0, 1.0))


class BulletController(Controller):
    def __init__(self, ship):
        '''state required for tracking control'''
        self.key_to_charging_bullet = {}
        self.ship = ship

    def control(self, key, press):
        '''dispatcher for entity state'''
        '''release = not press'''

        if key in [
            K_LEFT,
            K_RIGHT,
            K_UP,
            K_DOWN,
        ]:
            return

        key_name = pygame.key.name(key)
        if key not in [K_a, K_s, K_d, K_f]:
            return
        if press:
            if len(self.key_to_charging_bullet.keys()) > 3:
                return
            new_bullet = Bullet(Vector2(self.ship.pos.x, self.ship.pos.y), 1)
            self.key_to_charging_bullet[key_name] = new_bullet
        else:
            if key_name in self.key_to_charging_bullet:
                bullet = self.key_to_charging_bullet[key_name]
                bullet.release()
                random.choice(LASER_SOUNDS).play()
                self.ship.fly(Vector2(0.0, bullet.t*3.0))
                del self.key_to_charging_bullet[key_name]

    def step(self, t):
        for bullet in self.key_to_charging_bullet.values():
            bullet.charge(t)


def main():
    global PRIMARY_SURFACE
    global WINDOW
    global SHIP_SPRITES
    global PARTICLE_SPRITES
    global MOUSE_POSITION
    global LASER_SOUNDS
    global WARP_SOUNDS
    global MUSIC

    # PYGAME INIT, WINDOW SHIT
    pygame.init()
    PRIMARY_SURFACE = pygame.Surface(SCREEN_DIMS)
    WINDOW = pygame.display.set_mode(WINDOW_DIMS)
    # WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    # ASSET LOADING
    SHIP_SPRITES = SpriteSheet("./ships.png", 10, 10, 8, 8)
    PARTICLE_SPRITES = SpriteSheet("./particles.png", 6, 10, 8, 8)
    LASER_SOUNDS = [
        pygame.mixer.Sound('laserShoot1.wav'),
        pygame.mixer.Sound('laserShoot2.wav'),
        pygame.mixer.Sound('laserShoot3.wav'),
    ]
    MUSIC = [
        pygame.mixer.Sound('loading.wav'),
        pygame.mixer.Sound('menu.wav'),
    ]
    WARP_SOUNDS = [
        pygame.mixer.Sound('start_warping.wav'),
        pygame.mixer.Sound('stop_warping.wav'),
    ]

    # CLOCK
    clock = pygame.time.Clock()
    running = True
    lt = pygame.time.get_ticks()

    #   GAME STATE
    ship = Ship()
    star_field = StarField()
    ship_controller = ShipController(ship)
    bullet_controller = BulletController(ship)
    warp_controller = WarpController(star_field)
    controllers = []
    controllers.extend([ship_controller, bullet_controller, warp_controller])

    presstimes = {}
    MUSIC[0].play()
    MUSIC[1].play()
    while running:
        t = pygame.time.get_ticks()
        dt = (t - lt) / 1000.0
        lt = t

        mt = pygame.mouse.get_pos()
        MOUSE_POSITION = (Vector2(mt[0], mt[1]).elementwise() /
                          WINDOW_DIMS).elementwise() * SCREEN_DIMS

        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key in [K_ESCAPE, K_q]:
                    running = False

                name = pygame.key.name(event.key)
                if event.type == pygame.KEYDOWN:
                    presstimes[name] = t

                    for controller in controllers:
                        controller.control(event.key, press=True)

                elif event.type == pygame.KEYUP:
                    d = t - presstimes[name]
                    del presstimes[name]

                    # if d < PRESS_THRESHOLD:
                    #     print(f"{name} - pressed")
                    # else:
                    #     print(f"{name} - released after - {d}s")

                    for controller in controllers:
                        controller.control(event.key, press=False)

            if event.type == pygame.QUIT:
                running = False

        for controller in controllers:
            controller.step(t)

        PRIMARY_SURFACE.fill((0, 0, 0))

        star_field.step(dt)
        star_field.draw(ship)

        for bullet in BULLETS:
            if not bullet.moving:
                bullet.pos.x = ship.pos.x
                bullet.pos.y = ship.pos.y
                bullet.pos.y -= 8
            bullet.step(dt)
            bullet.draw()

        ship.step(dt)
        ship.draw()

        blit = pygame.transform.scale(PRIMARY_SURFACE, WINDOW.get_size())
        WINDOW.blit(blit, (0, 0))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
