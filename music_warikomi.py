import pygame
import time


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("sakekas.mp3")
    print("kokomade")
    pygame.mixer.music.play(1)
    time.sleep(1)
    pygame.mixer.music.stop()