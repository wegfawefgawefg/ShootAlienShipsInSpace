import controller


class BulletController(controller.Controller):
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
