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
