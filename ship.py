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
