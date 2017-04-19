# this defines all the tricks

from tricker import Tricker

class Trick():
    def __init__(self):
        # all tricks must rewrite these attributes
        # difficulty levels:
        # 1 - gainer, 540, btwist, tdr
        # 2 -

        self.difficulty = "WHY IS THIS NOT REWRITTEN"
        self.entryTransition = "WHY IS THIS NOT REWRITTEN"
        self.exitTransition = "WHY IS THIS NOT REWRITTEN"
        self.duration = "WHY IS THIS NOT REWRITTEN"

        tricker = Tricker()

    def getSweetSpots(self):
        pass

class Gainer(Trick):
    def __init__(self):
        super().__init__()
        self.duration = tricker.actor.getNumFrames('gainer')



