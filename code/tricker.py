# this is the class that defines the player character, and holds all of its animations
# + their animation timings

from direct.actor.Actor import Actor
from direct.task import Task
from tricks import *

from panda3d.core import *
# from direct.interval.IntervalGlobal import *


class Tricker(object):
    def __init__(self):
        # TODO: make a bad gswitch animation
        self.actor = Actor("tp/models/tricker-model",
                           {"gainer": "tp/anims/tricker-gainer",
                            "gainer_bad": "tp/anims/tricker-gainer-bad",
                            "gswitch": "tp/anims/tricker-gswitch",
                            "gswitch_bad": "tp/anims/tricker-gswitch"})

        #skillDict contains vals 1-100, percentage of skill in that trick
        self.skillDict = {"gainer": 0,
                          "gswitch": 0}


        # Load tricks
        self.gainer = Gainer(self)
        self.gswitch = Gswitch(self)

        # trickMap is different - this shit maps trick names to their classes
        # in order to get class data just given an animation name
        self.trickMap = {'gainer': self.gainer,
                         'gswitch': self.gswitch}

        self.prevTrick = None

        self.totalStam = self.stamina = 100

        self.grade = ' '

    def getGreenPercentage(self):
        currAnim = self.actor.getCurrentAnim()

        if currAnim:
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

    def stamPercentage(self):
        sp = self.stamina/self.totalStam
        if sp < 0 : sp = 0
        return sp

    def getGrade(self):
        return self.grade

    def tryTrick(self, trick, taskMgr):
        if self.stamina <= 0:
            print("no stamina!")
            return

        grade = 'A'
        currAnim = self.actor.getCurrentAnim()
        goodPercentage = trick.getGoodPercentage(grade)

        if currAnim:
            if self.prevTrick.getExitTransition() != trick.getEntryTransition():
                print("invalid transition")
                return
            currFrame = self.actor.getCurrentFrame(currAnim)
            numFrames = self.actor.getNumFrames(currAnim)
            framesLeft = numFrames - currFrame

            self.grade = self.prevTrick.getGrade(currFrame)
            if self.grade == 'E': return

            goodPercentage = trick.getGoodPercentage(grade)

            # 0.06 is the time it takes for 2 frames - smooth blending
            delayTime = framesLeft / 30 - 0.06
            taskMgr.doMethodLater(delayTime, self.doTrickTask, 'doTrick',
                             extraArgs=[str(trick), goodPercentage], appendTask=True)
        else:
            taskMgr.add(self.doTrickTask, 'doTrick',
                             extraArgs=[str(trick), goodPercentage], appendTask=True)


        stamCost = trick.getStamCost(grade)
        self.stamina -= stamCost

        self.prevTrick = trick


    def doTrickTask(self, animation, goodPercentage, task):
        airTime = self.actor.getNumFrames(animation) / 30
        moveInterval = self.actor.posInterval(airTime,
                                                Point3(0, .1, 0),
                                                other=self.actor)

        badAnim = str(animation + "_bad")

        self.actor.enableBlend()
        self.actor.setControlEffect(badAnim, 1- goodPercentage)
        self.actor.setControlEffect(animation, goodPercentage)
        self.actor.play(badAnim)
        self.actor.play(animation)
        self.actor.disableBlend()

        moveInterval.start()
        return Task.done