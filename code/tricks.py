# this defines all the tricks
"""
PROCEDURE FOR ADDING A NEW TRICK:
Define the class here
Add to list of animations
Add bad animation to list of animations
Add to tricker.trickMap
Add to skills dict in tricker.saveDict
Initialize with other tricks in tricker.updateAttributes()
Add event handler (self.accept) to play.py
"""


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
        self.distance = "WHY IS THIS NOT REWRITTEN"

    def hasDistance(self):
        return self.distance != "WHY IS THIS NOT REWRITTEN"

    def getDistance(self):
        return self.distance

    def getExitTransition(self):
        return self.exitTransition

    def getDifficulty(self):
        return self.difficulty

    def getDuration(self):
        return self.duration

    def getSweetSpot(self):
        return self.sweetSpot

    def getExitTransition(self):
        return self.exitTransition

    def getEntryTransition(self):
        return self.entryTransition

    def getGreenPercentage(self):
        currAnim = self.actor.getCurrentAnim()

        if currAnim:
            currFrame = self.actor.getCurrentFrame()
            dist = abs(self.sweetSpot - currFrame)
            eMargin = self.duration * .2 / self.difficulty

            if dist > eMargin:
                gp = 0
            else:
                gp = dist / eMargin

            return (gp, 1 - gp)
        else:
            return (0, 0)

    def getGrade(self, inputFrame):

        distFromSS = abs(self.sweetSpot - inputFrame)

        # print("sweetSpot:", self.sweetSpot)
        # print("inputFrame:", inputFrame)
        # print("distFromSS:", distFromSS)

        eMargin = self.duration * .2 / self.difficulty
        bMargin = eMargin * .3
        cMargin = eMargin * .6

        # print("eMargin = %d bMargin = %d cMargin = %d"
        # % (eMargin, bMargin, cMargin))

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

    def getStamCost(self, grade):
        halfCost = self.baseStamCost // 2
        modPercentage = self.skillModifier / 100
        reduction = halfCost * modPercentage

        if grade == 'A':
            addition = 0
        elif grade == 'B':
            addition = halfCost * (1 / 3)
        elif grade == 'C':
            addition = halfCost * (2 / 3)
        elif grade == 'D':
            addition = halfCost
        elif grade == 'E':
            addition = halfCost

        stamCost = self.baseStamCost - reduction + addition
        return stamCost

    # returns the percentage of the "good" animation to be played vs the bad animation
    # basically controls how pretty a move will look based on the timing and the player character's skill level
    def getGoodPercentage(self, grade):
        inverseSkillPercentage = 1 - (self.skillModifier / 100)
        if grade == 'A':
            b = 1
        elif grade == 'B':
            b = .7
        elif grade == 'C':
            b = .4
        elif grade == 'D':
            b = .1
        elif grade == 'E':
            b = 0

        goodPercentage = b - (inverseSkillPercentage * b)

        print("skillModifier:", self.skillModifier)
        print("grade:", grade)
        print("goodPercentage:", goodPercentage)
        return goodPercentage


class Gainer(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.actor.getNumFrames('gainer')
        self.difficulty = 1
        self.entryTransition = 'swing'
        self.exitTransition = 'reversal'
        self.baseStamCost = 10
        self.skillModifier = self.tricker.skillDict['gainer']
        self.sweetSpot = 23
        self.distance = (0, 0, 0)

    def __repr__(self):
        return 'gainer'


class Gswitch(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.actor.getNumFrames('gswitch')
        self.difficulty = 1
        self.entryTransition = 'swing'
        self.exitTransition = 'swing'
        self.baseStamCost = 10
        self.skillModifier = self.tricker.skillDict['gswitch']
        self.sweetSpot = 15
        self.distance = (0, 2, 0)

    def __repr__(self):
        return 'gswitch'


class Btwist(Trick):
    def __init__(self, tricker):
        super().__init__(tricker)
        self.duration = self.tricker.actor.getNumFrames('btwist')
        self.difficulty = 1
        self.entryTransition = 'reversal'
        self.exitTransition = 'swing'
        self.baseStamCost = 10
        self.skillModifier = self.tricker.skillDict['btwist']
        self.sweetSpot = 19
        self.distance = (0, 5, 0)

    def __repr__(self):
        return 'btwist'
