# this is the class that defines the player character, and holds all of its animations
# + their animation timings

from direct.actor.Actor import Actor
# from direct.interval.IntervalGlobal import *


class Tricker(object):
    def __init__(self):
        self.actor = Actor("tp/models/tricker-model",
                           {"gainer": "tp/anims/tricker-gainer",
                            "gswitch": "tp/anims/tricker-gswitch"})
