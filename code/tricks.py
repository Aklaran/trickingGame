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


        self.tricker = Tricker()

    def getGrade(self, inputFrame):
        sweetSpot = int(self.duration * .90)
        distFromSS = abs(sweetSpot-inputFrame)

        print("sweetSpot:", sweetSpot)
        print("inputFrame:", inputFrame)
        print("distFromSS:", distFromSS)

        eMargin = self.duration * .2 / self.difficulty
        bMargin = eMargin * .3
        cMargin = eMargin * .6

        print("eMargin = %d bMargin = %d cMargin = %d"
                % (eMargin, bMargin, cMargin))

        if distFromSS == 0:
            return 'A'
        elif distFromSS <= bMargin:
            return 'B'
        elif distFromSS <= cMargin:
            return 'C'
        elif distFromSS <= eMargin:
            return 'D'
        elif distFromSS > eMargin:
            return 'E'




class Gainer(Trick):
    def __init__(self):
        super().__init__()
        self.duration = self.tricker.actor.getNumFrames('gainer')
        self.difficulty = 1

class Gswitch(Trick):
    def __init__(self):
        super().__init__()
        self.duration = self.tricker.actor.getNumFrames('gswitch')
        self.difficulty = 1
