import pygame


class SoundPlayer:
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=2048,
    )

    sounds = {
        "niture": pygame.mixer.Sound("sounds/niture.mp3"),
        "theme": pygame.mixer.Sound("sounds/theme.mp3"),
    }

    def play(name):
        snd: pygame.mixer.Sound = SoundPlayer.sounds.get(name)
        if snd:
            snd.play()
