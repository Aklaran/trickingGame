# this is the class that defines the player character, and holds all of its animations
# + their animation timings

from direct.actor.Actor import Actor
from direct.task import Task
from tricks import *

from panda3d.core import *
# from direct.interval.IntervalGlobal import *


class Tricker(object):
    def __init__(self):
        self.actor = Actor("tp/models/tricker-model",
                           {"gainer": "tp/anims/tricker-gainer",
                            "gainer_bad": "tp/anims/tricker-gainer-bad",
                            "gswitch": "tp/anims/tricker-gswitch"})

        #trickDict contains vals 1-100, percentage of skill in that trick
        self.trickDict = {"gainer": 0,
                          "gswitch": 0}

        # Load tricks
        self.gainer = Gainer(self)
        self.gswitch = Gswitch(self)

        self.prevTrick = None

        self.totalStam = self.stamina = 100

        self.grade = ' '

    def stamPercentage(self):
        sp = self.stamina/self.totalStam
        if sp < 0 : sp = 0
        return sp

    def getGrade(self):
        return self.grade

    def tryTrick(self, animation, trick, taskMgr):
        if self.stamina <= 0:
            print("no stamina!")
            return

        grade = 'A'
        currAnim = self.actor.getCurrentAnim()
        badPercentage = trick.getBadPercentage(grade)

        if currAnim:
            if self.prevTrick.getExitTransition() != trick.getEntryTransition():
                print("invalid transition")
                return
            currFrame = self.actor.getCurrentFrame(currAnim)
            numFrames = self.actor.getNumFrames(currAnim)
            framesLeft = numFrames - currFrame

            self.grade = self.prevTrick.getGrade(currFrame)
            if self.grade == 'E': return

            badPercentage = trick.getBadPercentage(grade)

            # 0.06 is the time it takes for 2 frames - smooth blending
            delayTime = framesLeft / 30 - 0.06
            taskMgr.doMethodLater(delayTime, self.doTrickTask, 'doTrick',
                             extraArgs=[animation, badPercentage], appendTask=True)
        else:
            taskMgr.add(self.doTrickTask, 'doTrick',
                             extraArgs=[animation, badPercentage], appendTask=True)


        stamCost = trick.getStamCost(grade)
        self.stamina -= stamCost

        self.prevTrick = trick


    def doTrickTask(self, animation, badPercentage, task):
        airTime = self.actor.getNumFrames(animation) / 30
        moveInterval = self.actor.posInterval(airTime,
                                                Point3(0, .1, 0),
                                                other=self.actor)

        badAnim = str(animation + "_bad")

        self.actor.enableBlend()
        self.actor.setControlEffect(badAnim, 1- badPercentage)
        self.actor.setControlEffect(animation, badPercentage)
        self.actor.play(badAnim)
        self.actor.play(animation)
        self.actor.disableBlend()

        moveInterval.start()
        return Task.done