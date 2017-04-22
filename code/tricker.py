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

        self.trickList = {"gainer": 0,
                          "gswitch": 0}

        # Load tricks
        self.gainer = Gainer(self)
        self.gswitch = Gswitch(self)

        self.prevTrick = None

        self.stamina = 100

    def tryTrick(self, animation, trick, taskMgr):
        if self.stamina <= 0:
            print("no stamina!")
            return
        currAnim = self.actor.getCurrentAnim()
        if currAnim:
            if self.prevTrick.getExitTransition() != trick.getEntryTransition():
                print("invalid transition")
                return
            currFrame = self.actor.getCurrentFrame(currAnim)
            numFrames = self.actor.getNumFrames(currAnim)
            framesLeft = numFrames - currFrame

            grade = self.prevTrick.getGrade(currFrame)
            self.drawGrade(grade)
            # TODO: organize the grading system
            if grade == 'E': return

            # 0.06 is the time it takes for 2 frames - smooth blending
            delayTime = framesLeft / 30 - 0.06
            taskMgr.doMethodLater(delayTime, self.doTrickTask, 'doTrick',
                             extraArgs=[animation], appendTask=True)
        else:
             taskMgr.add(self.doTrickTask, 'doTrick',
                             extraArgs=[animation], appendTask=True)

        stamCost = trick.getStamCost()
        self.stamina -= stamCost

        self.prevTrick = trick


    def doTrickTask(self, animation, task):
        airTime = self.actor.getNumFrames(animation) / 30
        moveInterval = self.actor.posInterval(airTime,
                                                Point3(0, .1, 0),
                                                other=self.actor)
        self.actor.play(animation)

        moveInterval.start()
        return Task.done

    def drawGrade(self, grade):
        if grade == 'D':
            print('Grade: D. pretty shit.')
        elif grade == 'C':
            print('Grade: C. MEDIOCRE')
        elif grade == 'B':
            print('Grade: B. Aight')
        elif grade == 'A':
            print("Grade: A. PERFFECT")
        elif grade == 'E':
            print("Grade: E. Trick failed")