import random


class RandomUtils(object):

    @staticmethod
    def decision(probability):
        return random.random() < probability
