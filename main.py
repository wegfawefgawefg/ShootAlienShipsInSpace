import math
from pprint import pprint
import random

import math
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

import pymunk
from pymunk import Vec2d as pvec2

PRESS_THRESHOLD = 100

SCREEN_DIMS = Vector2(240, 160)
WINDOW_DIMS = SCREEN_DIMS * 4.0

PRIMARY_SURFACE = None
WINDOW = None

SHIP_SPRITES = None
PARTICLE_SPRITES = None
MAIN_MENU_ASSETS = None

LASER_SOUNDS = None
WARP_SOUNDS = None
MUSIC = None

MOUSE_POSITION = None
PHYSWORLD = None

GAME_STATE = "main_menu"

BULLETS = []


class StarField:
    def __init__(self):
        self.warp_level = 10.0
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
                self.remove(star)

    def remove(self, star):
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
    SPEED = 1600.0
    MAX_TYPE = 11
    MIN_LIFE = 0.02
    LIFE_SPAN_PER_TYPE = 0.04

    def __init__(self, pos, t) -> None:
        random.choice(LASER_SOUNDS).play()
        self.age = 0
        self.creation_time = pygame.time.get_ticks()
        self.id = Bullet.ID
        Bullet.ID += 1

        self.pos = pos
        self.pos.y - 8
        self.t = t
        BULLETS.append(self)

        mass = 10
        radius = 2
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = self.pos.x, self.pos.y
        self.shape = pymunk.Circle(body, radius, pvec2(0, 0))

        body.apply_impulse_at_local_point(pvec2(0.0, -Bullet.SPEED))
        PHYSWORLD.add(body, self.shape)

    def step(self, dt):
        # if self.moving:
        #     self.age += dt
        #     self.pos.y -= Bullet.MIN_SPEED + Bullet.SPEED_PER_TYPE * self.t

        if self.age > (Bullet.MIN_LIFE + Bullet.LIFE_SPAN_PER_TYPE * self.t):
            self.remove()
        if self.pos.y < 0:
            self.remove()

    def remove(self):
        for i in range(len(BULLETS)):
            bullet = BULLETS[i]
            if bullet.id == self.id:
                BULLETS.pop(i)
                break

        PHYSWORLD.remove(self.shape, self.shape.body)
        PHYSWORLD.remove(self.shape)

    def draw(self):
        p = self.get_pos()
        PARTICLE_SPRITES.draw_sprite(self.t, p.x, p.y)
        pygame.draw.circle(
            PRIMARY_SURFACE, (255, 0, 0), (p.x, p.y),
            self.shape.radius, 1
        )

    def get_pos(self):
        return self.shape.body.position


class KillZones:
    def __init__(self) -> None:
        self.right_shape = self.make_body(
            (SCREEN_DIMS.x, 0), (SCREEN_DIMS.x, SCREEN_DIMS.y))
        self.left_shape = self.make_body((-1, 0), (-1, SCREEN_DIMS.y))
        self.back_shape = self.make_body((0, 0), (SCREEN_DIMS.x, 0))
        self.front_shape = self.make_body(
            (0, SCREEN_DIMS.y), (SCREEN_DIMS.x, SCREEN_DIMS.y))

    def make_body(self, a, b):
        line_moment = pymunk.moment_for_segment(0, a, b, 10)
        line_body = pymunk.Body(1, line_moment, body_type=pymunk.Body.STATIC)
        # line_body.position = a
        line_shape = pymunk.Segment(line_body, a, b, 1)
        PHYSWORLD.add(line_body, line_shape)
        return line_shape

    def step(dt):
        pass

    def draw_line(self, shape):
        pygame.draw.line(
            PRIMARY_SURFACE, (255, 0, 0),
            (shape.a.x, shape.a.y),
            (shape.b.x, shape.b.y),
            1
        )

    def draw(self):
        pass
        # self.draw_line(self.left_shape)
        # self.draw_line(self.right_shape)
        # self.draw_line(self.back_shape)
        # self.draw_line(self.front_shape)


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
        if press and key == K_f:
            new_bullet = Bullet(Vector2(self.ship.pos.x, self.ship.pos.y), 1)

    def step(self, t):
        for bullet in self.key_to_charging_bullet.values():
            bullet.charge(t)


def do_main_menu():
    global PRIMARY_SURFACE
    global WINDOW
    global MUSIC
    global MAIN_MENU_ASSETS
    global GAME_STATE

    clock = pygame.time.Clock()
    lt = pygame.time.get_ticks()

    MUSIC[2].play(loops=-1)

    size = SCREEN_DIMS * 1.2
    mm_background = pygame.transform.scale(
        MAIN_MENU_ASSETS[0], (size.x, size.y))

    tsize = SCREEN_DIMS * 1.2
    mm_title = pygame.transform.scale(
        MAIN_MENU_ASSETS[1], (tsize.x, tsize.y))

    tbsize = tsize * 1.1
    mm_title_behind = pygame.transform.scale(
        MAIN_MENU_ASSETS[1], (tbsize.x, tbsize.y))
    mm_title_behind.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    mm_title_behind.set_alpha(220)

    running = True
    while running:
        t = pygame.time.get_ticks()
        dt = (t - lt) / 1000.0
        lt = t

        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN]:
                if event.key in [K_ESCAPE, K_q]:
                    running = False
                    return False
                else:
                    GAME_STATE = "game"
                    return True
            if event.type == pygame.QUIT:
                return False

        PRIMARY_SURFACE.fill((255, 0, 0))
        offset = SCREEN_DIMS.y / 10.0
        background_y = 0.3*math.sin(t*0.003)*offset - offset * 1.5
        background_x = 0.3*math.sin(t*0.0013)*offset - offset * 1.5
        PRIMARY_SURFACE.blit(mm_background, (background_x, background_y))

        t_o = -SCREEN_DIMS * 0.1

        title_y = 0.5 + math.sin(t*0.001)*0.5
        title_y *= SCREEN_DIMS.y * 0.05
        title_y -= title_y * 0.5

        PRIMARY_SURFACE.blit(mm_title_behind, (t_o.x, title_y+t_o.y))
        PRIMARY_SURFACE.blit(
            mm_title, (t_o.x - t_o.x * 0.4, title_y+t_o.y - t_o.y * 0.2))

        blit = pygame.transform.scale(PRIMARY_SURFACE, WINDOW.get_size())
        WINDOW.blit(blit, (0, 0))
        pygame.display.flip()
    return True


def do_main_game():
    global PRIMARY_SURFACE
    global WINDOW
    global SHIP_SPRITES
    global PARTICLE_SPRITES
    global MOUSE_POSITION
    global LASER_SOUNDS
    global WARP_SOUNDS
    global MUSIC
    global MAIN_MENU_ASSETS
    global GAME_STATE
    global PHYSWORLD

    PHYSWORLD = pymunk.Space()

    #   GAME STATE
    ship = Ship()
    star_field = StarField()
    ship_controller = ShipController(ship)
    bullet_controller = BulletController(ship)
    warp_controller = WarpController(star_field)
    controllers = []
    controllers.extend([ship_controller, bullet_controller, warp_controller])

    mt = pygame.mouse.get_pos()
    MOUSE_POSITION = (Vector2(mt[0], mt[1]).elementwise() /
                      WINDOW_DIMS).elementwise() * SCREEN_DIMS

    class Debris:
        def __init__(self) -> None:
            mass = 10
            radius = 3
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            center = SCREEN_DIMS // 2
            body.position = center.x, center.y
            self.shape = pymunk.Circle(body, radius, pvec2(0, 0))

            PHYSWORLD.add(body, self.shape)

        def get_pos(self):
            return self.shape.body.position

        def draw(self):
            p = self.get_pos()
            pygame.draw.circle(
                PRIMARY_SURFACE, (255, 0, 0), (p.x, p.y),
                self.shape.radius, 1
            )
            SHIP_SPRITES.draw_sprite(4, p.x, p.y)

        def remove(self):
            PHYSWORLD.remove(self.shape, self.shape.body)
            PHYSWORLD.remove(self.shape)

        def step(self):
            pass

    # CLOCK
    clock = pygame.time.Clock()
    lt = pygame.time.get_ticks()

    MUSIC[0].play(loops=-1)
    MUSIC[1].play(loops=-1)

    enemies = []
    enemies.append(Debris())
    enemies.append(Debris())
    enemies.append(Debris())
    enemies.append(Debris())
    kill_zones = KillZones()

    presstimes = {}
    running = True
    while running:
        t = pygame.time.get_ticks()
        dt = (t - lt) / 1000.0
        lt = t

        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key in [K_ESCAPE, K_q]:
                    MUSIC[0].stop()
                    MUSIC[1].stop()
                    GAME_STATE = "main_menu"
                    return True

                name = pygame.key.name(event.key)
                if event.type == pygame.KEYDOWN:
                    presstimes[name] = t

                    for controller in controllers:
                        controller.control(event.key, press=True)

                elif event.type == pygame.KEYUP:
                    if name not in presstimes:
                        continue
                    d = t - presstimes[name]
                    del presstimes[name]

                    # if d < PRESS_THRESHOLD:
                    #     print(f"{name} - pressed")
                    # else:
                    #     print(f"{name} - released after - {d}s")

                    for controller in controllers:
                        controller.control(event.key, press=False)

            if event.type == pygame.QUIT:
                MUSIC[0].stop()
                MUSIC[1].stop()
                GAME_STATE = "main_menu"
                return True

        for controller in controllers:
            controller.step(t)

        PHYSWORLD.step(dt)

        PRIMARY_SURFACE.fill((0, 0, 0))

        star_field.step(dt)
        star_field.draw(ship)

        for bullet in BULLETS:
            bullet.step(dt)
            bullet.draw()

        for enemy in enemies:
            enemy.step()
            enemy.draw()

        kill_zones.step()
        kill_zones.draw()

        ship.step(dt)
        ship.draw()

        blit = pygame.transform.scale(PRIMARY_SURFACE, WINDOW.get_size())
        WINDOW.blit(blit, (0, 0))
        pygame.display.flip()
    return True


def main():
    global PRIMARY_SURFACE
    global WINDOW
    global SHIP_SPRITES
    global PARTICLE_SPRITES
    global MOUSE_POSITION
    global LASER_SOUNDS
    global WARP_SOUNDS
    global MUSIC
    global MAIN_MENU_ASSETS
    global GAME_STATE

    # PYGAME INIT, WINDOW SHIT
    pygame.init()
    PRIMARY_SURFACE = pygame.Surface(SCREEN_DIMS)
    WINDOW = pygame.display.set_mode(WINDOW_DIMS)
    # WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)

    # ASSET LOADING
    SHIP_SPRITES = SpriteSheet("assets/ships.png", 10, 10, 8, 8)
    PARTICLE_SPRITES = SpriteSheet("assets/particles.png", 6, 10, 8, 8)
    LASER_SOUNDS = [
        pygame.mixer.Sound('assets/laserShoot1.wav'),
        pygame.mixer.Sound('assets/laserShoot2.wav'),
        pygame.mixer.Sound('assets/laserShoot3.wav'),
    ]
    MUSIC = [
        pygame.mixer.Sound('assets/loading.wav'),
        pygame.mixer.Sound('assets/menu.wav'),
        pygame.mixer.Sound('assets/mainmenumusic.wav'),
    ]
    WARP_SOUNDS = [
        pygame.mixer.Sound('assets/start_warping.wav'),
        pygame.mixer.Sound('assets/stop_warping.wav'),
    ]
    MAIN_MENU_ASSETS = [
        pygame.image.load('assets/cover.png'),
        pygame.image.load('assets/title.png')
    ]

    running = True
    while running:
        if GAME_STATE == "main_menu":
            running = do_main_menu()
        elif GAME_STATE == "game":
            running = do_main_game()
    pygame.quit()


if __name__ == '__main__':
    main()
