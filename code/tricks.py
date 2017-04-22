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
        self.baseStamCost = "WHY IS THIS NOT REWRITTEN"
        self.skillModifier = "WHY IS THIS NOT REWRITTEN"

    def getExitTransition(self):
        return self.exitTransition
    def getEntryTransition(self):
        return self.entryTransition

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

    def getStamCost(self):
        halfCost = self.baseStamCost // 2
        modPercentage = self.skillModifier / 100
        reduction = halfCost * modPercentage

        return self.baseStamCost - reduction




class Gainer(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.actor.getNumFrames('gainer')
        self.difficulty = 1
        self.entryTransition = 'swing'
        self.exitTransition = 'reversal'
        self.baseStamCost = 10
        self.skillModifier = self.tricker.trickList['gainer']

class Gswitch(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.actor.getNumFrames('gswitch')
        self.difficulty = 2
        self.entryTransition = 'swing'
        self.exitTransition = 'swing'
        self.baseStamCost = 10
        self.skillModifier = self.tricker.trickList['gswitch']