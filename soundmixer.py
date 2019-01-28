from os import listdir
from os.path import isfile, join

import pygame

from settings import SOUNDS_DIR, SOUNDTRACK


def init_mixer():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)
    pygame.mixer.Channel(0).set_volume(0.3)
    pygame.mixer.set_reserved(0)
    pygame.mixer.set_reserved(1)
    pygame.mixer.map = \
        {key: pygame.mixer.Sound(key) for key in
         [SOUNDS_DIR + f for f in listdir(SOUNDS_DIR) if isfile(join(SOUNDS_DIR, f))]}


def setmusic():
    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(0).play(pygame.mixer.map[SOUNDTRACK])


def update():
    # if soundtrack has ended replay
    if not pygame.mixer.Channel(0).get_busy():
        pygame.mixer.Channel(0).play(pygame.mixer.map[SOUNDTRACK])


def stopmusic():
    pygame.mixer.Channel(0).stop()


def queueeffect(effect):
    pygame.mixer.Channel(2).queue(pygame.mixer.map[effect])


def solochanneleffect(effect):
    # look for free channel and play, soundtrack channel 1 and queue channel 2 excluded
    channel = pygame.mixer.find_channel()
    if channel is not None:
        channel.play(pygame.mixer.map[effect])
