import random

import pygame

import entity

'''
add dict of bullets to scene
put ids in the entity class so you dont repeat them
'''


class Bullet(entity.Entity):
    ID = 0
    SPEED = 1600.0
    MAX_TYPE = 11
    MIN_LIFE = 0.02
    LIFE_SPAN_PER_TYPE = 0.04

    def __init__(self, scene, pos, t) -> None:
        super.__init__(scene)

        assets = scene.game.assets

        random.choice(assets.LASER_SOUNDS).play()
        self.age = 0
        self.creation_time = pygame.time.get_ticks()
        self.id = Bullet.ID
        Bullet.ID += 1

        self.pos = pos
        self.pos.y - 8
        self.t = t
        scene.bullets.append(self)

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
