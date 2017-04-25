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

            if dist > eMargin: gp = 0
            else: gp = dist/eMargin

            return (gp, 1-gp)
        else:
            return (0,0)

    def getGrade(self, inputFrame):

        distFromSS = abs(self.sweetSpot-inputFrame)

        #print("sweetSpot:", self.sweetSpot)
        #print("inputFrame:", inputFrame)
        #print("distFromSS:", distFromSS)

        eMargin = self.duration * .2 / self.difficulty
        bMargin = eMargin * .3
        cMargin = eMargin * .6

        #print("eMargin = %d bMargin = %d cMargin = %d"
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
            addition = halfCost * (1/3)
        elif grade == 'C':
            addition = halfCost * (2/3)
        elif grade == 'D':
            addition = halfCost

        stamCost = self.baseStamCost - reduction + addition
        return stamCost

    # returns the percentage of the "good" animation to be played vs the bad animation
    # basically controls how pretty a move will look based on the timing and the player character's skill level
    def getGoodPercentage(self, grade):
        inverseSkillPercentage = 1- (self.skillModifier / 100)
        if grade == 'A': base = 1
        elif grade == 'B': base = .7
        elif grade == 'C': base = .4
        elif grade == 'D': base = .1

        goodPercentage = base - (inverseSkillPercentage * base)

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
        self.sweetSpot = int(self.duration * .80)
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
        self.sweetSpot = int(self.duration * .80)
    def __repr__(self):
        return 'gswitch'