import controller


class WarpController(controller.Controller):
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
