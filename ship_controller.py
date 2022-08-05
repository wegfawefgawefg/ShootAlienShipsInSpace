import controller


class ShipController(controller.Controller):
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
