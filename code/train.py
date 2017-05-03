from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.gui.DirectGui import *

from panda3d.core import *

from math import *

from play import Play


class TrainingMode(Play):
    def __init__(self):
        super().__init__()

        taskMgr.add(self.drawUITask, 'drawUI', extraArgs=['train'],
                    appendTask=True)
        taskMgr.add(self.checkGameStateTask, 'checkGameState')
        self.showInitialDialog()

    def showInitialDialog(self):
        initialStr = "- TRAINING MODE - \n" \
                     "Use shift/ctrl + [U, I, O, P] to execute some cool ass tricks. \n" \
                     "As the timing bar fills up, hit another key to chain tricks together. \n" \
                     "Experiment with cool combos and build your skill! \n" \
                     "To see the whole control scheme, check the controls tab in the main menu."

        self.initialDialog = DirectDialog(dialogName="initialDialog", scale=1,
                                          text=initialStr,
                                          buttonTextList=['Start training!'],
                                          command=self.closeInitialDialog)

    def closeInitialDialog(self, arg):
        self.initialDialog.detachNode()

    def checkGameStateTask(self, task):
        if base.currPlayer.comboHasEnded():
            taskMgr.doMethodLater(2, self.reset, 'reset')
            return Task.done
        if base.currPlayer.isFalling():
            taskMgr.doMethodLater(3, self.reset, 'reset')
            return Task.done
        return Task.cont

    def reset(self, task):
        taskMgr.remove("follow")
        base.currPlayer.actor.setPos(0, 0, 0)
        base.currPlayer.actor.pose('btwist', 1)
        self.trickerDummyNode.setPos(base.currPlayer.actor, (0,0,3))
        base.currPlayer.reset()

        taskMgr.add(self.FollowCamTask, 'follow')
        taskMgr.add(self.checkGameStateTask, 'checkGameState')

        return Task.done

    def destroy(self):
        super().destroy()



