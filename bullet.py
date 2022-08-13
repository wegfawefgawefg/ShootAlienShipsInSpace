import random

import pygame
import pymunk
from pymunk.vec2d import Vec2d as pvec2

import entity
from enums import CollisionType

"""
add dict of bullets to scene
put ids in the entity class so you dont repeat them
"""

def remove_bullet(arbiter, space, data):
    bullet_shape = arbiter.shapes[1]
    if hasattr(bullet_shape, "entity"):
        bullet = bullet_shape.entity
        assert type(bullet) == Bullet
        bullet.scene.remove_entity(bullet)

    return True

class Bullet(entity.Entity):
    SPEED = 1600.0
    MAX_TYPE = 11
    MIN_LIFE = 0.02
    LIFE_SPAN_PER_TYPE = 0.04

    def __init__(self, scene, pos, t) -> None:
        super().__init__(scene)

        random.choice(self.scene.game.sounds.laser_sounds).play()
        self.age = 0
        self.creation_time = pygame.time.get_ticks()

        self.pos = pos
        self.pos.y - 8
        self.t = t

        self.create_physics_objects()
        self.body.apply_impulse_at_local_point(pvec2(0.0, -Bullet.SPEED))

    def create_physics_objects(self):
        mass = 10
        radius = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        
        self.body = self.add_physics_object(pymunk.Body(mass, inertia))
        self.body.position = self.pos.x, self.pos.y

        self.shape = self.add_physics_object(pymunk.Circle(self.body, radius, pvec2(0, 0)))
        self.shape.collision_type = CollisionType.BULLET.value

        self.scene.physics.add(self.body, self.shape)

        ch = self.scene.physics.add_collision_handler(
            CollisionType.BULLET.value, CollisionType.DEBRIS.value
        )
        ch.begin = remove_bullet

        self.shape.entity = self

    def step(self):
        if self.age > (Bullet.MIN_LIFE + Bullet.LIFE_SPAN_PER_TYPE * self.t):
            self.remove()
        if self.pos.y < 0:
            self.remove()

    def draw(self):
        p = self.get_pos()
        self.scene.game.graphics.draw_sprite(
            self.scene.game.sprite_sheets.particles, self.t, p.x, p.y
        )
        # pygame.draw.circle(
        #     self.scene.game.graphics.primary_surface,
        #     (255, 0, 0),
        #     (p.x, p.y),
        #     self.shape.radius,
        #     1,
        # )

    def get_pos(self):
        return self.shape.body.position
