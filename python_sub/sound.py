import pygame


class SoundPlayer:
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=2048,
    )

    sounds = {
        "bureki":pygame.mixer.Sound("sounds/bureki.mp3"),
        "burekiyo":pygame.mixer.Sound("sounds/burekiyo.mp3"),
        "hidari":pygame.mixer.Sound("sounds/hidari.mp3"),
        "kaishi":pygame.mixer.Sound("sounds/kaishi.mp3"),
        "kakudo1":pygame.mixer.Sound("sounds/kakudo1.mp3"),
        "kakudo2":pygame.mixer.Sound("sounds/kakudo2.mp3"),
        "kakudo3":pygame.mixer.Sound("sounds/kakudo3.mp3"),
        "kakudo4":pygame.mixer.Sound("sounds/kakudo4.mp3"),
        "kakudo5":pygame.mixer.Sound("sounds/kakudo5.mp3"),
        "kakudoage":pygame.mixer.Sound("sounds/kakudoage.mp3"),
        "kakudosage":pygame.mixer.Sound("sounds/kakudosage.mp3"),
        "koutai":pygame.mixer.Sound("sounds/koutai.mp3"),
        "migi":pygame.mixer.Sound("sounds/migi.mp3"),
        "sokudo1":pygame.mixer.Sound("sounds/sokudo1.mp3"),
        "sokudo2":pygame.mixer.Sound("sounds/sokudo2.mp3"),
        "sokudo3":pygame.mixer.Sound("sounds/sokudo3.mp3"),
        "sokudo4":pygame.mixer.Sound("sounds/sokudo4.mp3"),
        "sokudo5":pygame.mixer.Sound("sounds/sokudo5.mp3"),
        "sokudoage":pygame.mixer.Sound("sounds/sokudoage.mp3"),
        "sokudosage":pygame.mixer.Sound("sounds/sokudosage.mp3"),
        "syomen":pygame.mixer.Sound("sounds/syomen.mp3"),
        "syuryo":pygame.mixer.Sound("sounds/syuryo.mp3"),
        "teishi":pygame.mixer.Sound("sounds/teishi.mp3"),
        "zenshin":pygame.mixer.Sound("sounds/zenshin.mp3"),
    }

    def play(name):
        snd: pygame.mixer.Sound = SoundPlayer.sounds.get(name)
        if snd:
            snd.play()
