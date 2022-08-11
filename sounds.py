import pygame


class Sounds:
    def __init__(self) -> None:
        self.laser_sounds = [
            pygame.mixer.Sound("assets/laserShoot1.wav"),
            pygame.mixer.Sound("assets/laserShoot2.wav"),
            pygame.mixer.Sound("assets/laserShoot3.wav"),
        ]
        self.start_warp = pygame.mixer.Sound("assets/start_warping.wav")
        self.stop_warp = pygame.mixer.Sound("assets/stop_warping.wav")
