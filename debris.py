import random

from icecream import ic
import pygame
import pymunk
from pymunk import Vec2d as pvec2

from entity import Entity
from enums import CollisionType

def hit_by_bullet(arbiter, space, data):
    debris_shape = arbiter.shapes[0]
    if hasattr(debris_shape, "entity"):
        debris = debris_shape.entity
        assert type(debris) == Debris
        debris.scene.remove_entity(debris)
        random.choice(debris.scene.game.sounds.rock_hit_by_laser).play()

        # if debris.depth == 0:
        for _ in range(4):
            Debris(debris.scene).set_depth(depth=1)

    return True

class Debris(Entity):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.create_physics_objects()
        self.set_depth()

    def set_depth(self, depth=0):
        self.depth = depth

    def create_physics_objects(self):
        mass = 10
        radius = 3
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = self.add_physics_object(pymunk.Body(mass, inertia))
        
        p = self.scene.game.graphics.get_random_place_on_screen()
        self.body.position = p.x, p.y
        self.shape = self.add_physics_object(pymunk.Circle(self.body, radius, pvec2(0, 0)))
        self.shape.collision_type = CollisionType.DEBRIS.value
        self.scene.physics.add(self.body, self.shape)

        ch = self.scene.physics.add_collision_handler(
            CollisionType.DEBRIS.value, CollisionType.BULLET.value
        )
        ch.post_solve = hit_by_bullet 
        '''
        consider a self function here, but i think it doesnt work 
        likely all collisions will somehow ref this object instead of themself
        '''
        self.shape.entity = self

    def get_pos(self):
        return self.body.position

    def draw(self):
        p = self.get_pos()
        pygame.draw.circle(
            self.scene.game.graphics.primary_surface,
            (255, 0, 0),
            (p.x, p.y),
            self.shape.radius,
            1,
        )
        self.scene.game.graphics.draw_sprite(
            self.scene.game.sprite_sheets.ships, 4, p.x, p.y
        )

    def remove(self):
        self.scene.physics.remove(self.shape, self.body)
        self.scene.physics.remove(self.shape)

    def step(self):
        pass
