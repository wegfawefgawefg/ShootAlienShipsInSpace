import scene


class SpaceBattle(scene.Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def control(self, event):
        pass

    def step(self):
        pass

    def draw(self):
        pass

    def exit(self):
        pass


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

    PRIMARY_SURFACE = pygame.Surface(SCREEN_DIMS)

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
