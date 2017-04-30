from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import *
from direct.interval.IntervalGlobal import Sequence, Func
from direct.interval.ActorInterval import ActorInterval


from tricks import *

import math


class Tricker(object):
    def __init__(self):
        ## tricker-model taken from tutorial files from
        # https://www.digitaltutors.com/tutorial/1478-Animating-an-Acrobatic-Fight-Scene-in-Maya
        self.actor = Actor("tp/models/tricker-model",
                           {"gainer"         : "tp/anims/tricker-gainer",
                            "gainer_bad"     : "tp/anims/tricker-gainer-bad",
                            "gswitch"        : "tp/anims/tricker-gswitch",
                            "gswitch_bad"    : "tp/anims/tricker-gswitch",
                            "btwist"         : "tp/anims/tricker-btwist",
                            "btwist_bad"     : "tp/anims/tricker-btwist",
                            "cork"           : "tp/anims/tricker-cork",
                            "cork_bad"       : "tp/anims/tricker-cork",
                            "doublecork"     : "tp/anims/tricker-dubcork",
                            "doublecork_bad" : "tp/anims/tricker-dubcork",
                            "fall_swing"     : "tp/anims/tricker-fall-left"})

        #saveDict contains all info to be saved to json
        self.saveDict = { 'name': '',
                          'level': 0,
                          'totalStam': 100,
                          'skills': { "gainer"     : 1,
                                      "gswitch"    : 1,
                                      "btwist"     : 1,
                                      "cork"       : 1,
                                      "doublecork" : 1}
                          }
        self.updateAttributes()

        # trickMap is different - this shit maps trick names to their classes
        # in order to get class data just given an animation name
        self.trickMap = {'gainer'     : self.gainer,
                         'gswitch'    : self.gswitch,
                         'btwist'     : self.btwist,
                         'cork'       : self.cork,
                         'doublecork' : self.doublecork}


        # runtime traits, to be reset with reset function
        # NOTE: You MUST add any vals here to the reset function below
        self.prevTrick = None
        self.stamina = self.totalStam
        self.grade = ''
        self.timing = ''
        self.score = 0
        self.comboLength = 0
        self.comboEnded = False
        self.comboContinuing = False
        self.falling = False

    def comboHasEnded(self):
        return self.comboEnded
    def hasName(self):
        return self.name != ''
    def isFalling(self):
        return self.falling
    def getName(self):
        if self.hasName(): return self.name
        else: return "NewPlayer"
    def getSaveDict(self):
        return self.saveDict
    def getSkillDict(self):
        return self.skillDict
    def getComboLength(self):
        return str(int(self.comboLength))
    def getScore(self):
        return str(int(self.score))
    def getTiming(self):
        return self.timing

    def updateStamina(self, stamCost):
        self.stamina -= stamCost
    def updateComboLength(self):
        self.comboLength += 1
    def updateScore(self, trick, goodPercentage, comboLength):
        b = trick.getDifficulty() * 100
        score = b + (b*goodPercentage) + (b*(comboLength/5))
        self.score += score

    def getTimingBarPercentage(self):
        currAnim = self.actor.getCurrentAnim()

        if currAnim and 'fall' not in currAnim:
            trick = self.trickMap[currAnim.split('_')[0]]
            sweetspot = trick.getSweetSpot()
            currFrame = self.actor.getCurrentFrame()
            dist = abs(sweetspot - currFrame)
            eMargin = trick.getDuration() * .2 / trick.getDifficulty()

            if dist > eMargin: gp = 0
            else: gp = 1- (dist/eMargin)

            return gp
        else:
            return 0

    def getTrueStam(self):
        return self.stamina

    def stamPercentage(self):
        sp = self.stamina/self.totalStam
        if sp < 0 : sp = 0
        return sp

    def getGrade(self):
        return self.grade

    def increaseSkill(self, trick, grade):
        if grade == 0: b = 2
        elif grade == 1: b = 1.66
        elif grade == 2: b = 1.33
        elif grade == 3: b = 1
        elif grade == 4: b = 1

        # This line makes the exp curve and prevents leveling over 100
        exp = b - math.log(self.saveDict['skills'][str(trick)])

        if exp < 0: exp = 0

        self.saveDict['skills'][str(trick)] += exp
        self.updateAttributes()

    """
    debug animation procedure:
    comment out:
    return under if self.comboEnded in self.tryTrick
    both moveInterval.start() in self.doTrickTask
    
    
    """

    def tryTrick(self, trick, taskMgr):
        print("currPlayer:", base.currPlayer.getName())
        print("me: ", self.getName())
        if self.comboEnded:
            print("combo ended - no more tricking 4 u")
            return

        if self.falling:
            print("can't trick once you've fallen boi")
            return

        if self.stamina <= 0:
            self.comboEnded = True
            print("no stamina to throw trick!! ending combo")
            return

        self.comboContinuing = True
        distance = (0,0,0)

        self.grade = 0
        currAnim = self.actor.getCurrentAnim()
        goodPercentage = trick.getGoodPercentage(self.grade)

        if self.prevTrick: distance = self.prevTrick.getDistance()

        if currAnim and self.prevTrick:
            if (self.prevTrick.getExitTransition() != trick.getEntryTransition()):
                self.comboEnded = True
                print("invalid transition - ended combo")
                return

            distance = self.prevTrick.getDistance()

            currFrame = self.actor.getCurrentFrame(currAnim)
            numFrames = self.actor.getNumFrames(currAnim)
            framesLeft = numFrames - currFrame

            (self.grade, self.timing) = self.prevTrick.getGrade(currFrame)
            if self.grade == 4:
                self.falling = True
                print("Combo failed - falling")
                self.prevTrick = None

            stamCost = trick.getStamCost(self.grade)
            self.updateStamina(stamCost)

            goodPercentage = trick.getGoodPercentage(self.grade)

            # 0.06 is the time it takes for 2 frames - smooth blending
            delayTime = framesLeft / 30 - 0.09
            taskMgr.doMethodLater(delayTime, self.doTrickTask, 'doTrick',
                             extraArgs=[str(trick), goodPercentage, distance, taskMgr], appendTask=True)
        else:
            stamCost = trick.getStamCost(self.grade)
            self.updateStamina(stamCost)
            taskMgr.add(self.doTrickTask, 'doTrick',
                             extraArgs=[str(trick), goodPercentage, distance, taskMgr], appendTask=True)

        if self.getTrueStam() < 0:                             
            self.falling = True
            return("Ran out of stamina mid-trick - falling!")

        if not self.falling:
            self.updateScore(trick, goodPercentage, self.comboLength)
            self.updateComboLength()
            self.prevTrick = trick

        # this is tricking - you still learn from your falls!
        self.increaseSkill(trick, self.grade)

    def doTrickTask(self, animation, goodPercentage, distance, taskMgr, task):
        self.actor.setPos(self.actor, distance)
        badAnim = str(animation + "_bad")

        if not self.isFalling():
            self.actor.enableBlend()
            self.actor.setControlEffect(badAnim, 1- goodPercentage)
            self.actor.setControlEffect(animation, goodPercentage)
            self.actor.play(badAnim)
            self.actor.play(animation)
            self.actor.disableBlend()

            self.comboContinuing = False
            taskMgr.add(self.checkTrickStateTask, 'checkTrickState',
                        extraArgs=[animation], appendTask=True)

        elif self.isFalling():
            trick = self.trickMap[animation]
            exitTrans = trick.getExitTransition()
            fallingAnim = "fall_" + exitTrans

            fallStartFrame = 5
            regFrames = self.actor.getNumFrames(animation) - fallStartFrame

            fallSeq = Sequence(self.actor.actorInterval(badAnim, endFrame=regFrames),
                               Func(self.playFall, badAnim, fallingAnim, regFrames))
            fallSeq.start()

       # if moveInterval: moveInterval.start()
        return Task.done

    def playFall(self, badAnim, fallingAnim, startFrame):
        self.actor.enableBlend()
        self.actor.setControlEffect(badAnim, .5)
        self.actor.setControlEffect(fallingAnim, .5)
        self.actor.play(badAnim, fromFrame=startFrame)
        self.actor.play(fallingAnim)
        self.actor.disableBlend()

    def checkTrickStateTask(self, animation, task):
        # has to be -1 otherwise the currFrame never gets to the last frame. IDK why
        totalFrames = self.actor.getNumFrames(animation)-1
        currFrame = self.actor.getCurrentFrame(animation)


        if self.comboContinuing or self.falling:
            print("comboContinuing or falling")
            return Task.done
        self.comboContinuing = False
        if currFrame == totalFrames:
            self.comboEnded = True
            print("no input received - combo ended")
            return Task.done
        return Task.cont

    def reset(self):
        self.prevTrick = None
        self.stamina = 100
        self.grade = ''
        self.timing = ''
        self.score = 0
        self.comboLength = 0
        self.comboEnded = False
        self.comboContinuing = False
        self.falling = False

    def setName(self, name):
        self.saveDict['name'] = name
        self.updateAttributes()

    def loadToSaveDict(self, indata):
        self.saveDict = indata
        self.updateAttributes()

    def updateAttributes(self):
        self.name = self.saveDict['name']
        self.totalStam = self.saveDict['totalStam']
        self.skillDict = self.saveDict['skills']

        # set tricker's level based on proficiency in all skills
        numTricks = totalSP = 0
        for trick in self.skillDict:
            numTricks += 1
            totalSP += self.skillDict[trick]
        self.level = int(totalSP / numTricks)
        self.saveDict['level'] = self.level

        # Load tricks
        self.gainer = Gainer(self)
        self.gswitch = Gswitch(self)
        self.btwist = Btwist(self)
        self.cork = Cork(self)
        self.doublecork = DoubleCork(self)
