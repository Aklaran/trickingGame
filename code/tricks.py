# this defines all the tricks



class Trick():
    def __init__(self, tricker):

        self.tricker = tricker

        # all tricks must rewrite these attributes
        # difficulty levels:
        # 1 - gainer, 540, btwist, tdr
        # 2 -

        self.difficulty = "WHY IS THIS NOT REWRITTEN"
        self.entryTransition = "WHY IS THIS NOT REWRITTEN"
        self.exitTransition = "WHY IS THIS NOT REWRITTEN"
        self.duration = "WHY IS THIS NOT REWRITTEN"

    def getGrade(self, inputFrame):
        sweetSpot = int(self.duration * .80)
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

    def getExitTransition(self):
        return self.exitTransition
    def getEntryTransition(self):
        return self.entryTransition



class Gainer(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.getNumFrames('gainer')
        self.difficulty = 1
        self.entryTransition = 'swing'
        self.exitTransition = 'reversal'

class Gswitch(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.getNumFrames('gswitch')
        self.difficulty = 1
        self.entryTransition = 'swing'
        self.exitTransition = 'swing'