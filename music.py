import pygame


class Music:
    def __init__(self) -> None:
        self.main_menu_song = pygame.mixer.Sound('assets/mainmenumusic.wav')
        self.space_battle_songs = [
            pygame.mixer.Sound('assets/loading.wav'),
            pygame.mixer.Sound('assets/menu.wav'),
        ]
