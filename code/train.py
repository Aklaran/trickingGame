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
        self.ignoreAll()
        taskMgr.remove('follow')
        taskMgr.remove('drawUI')
        taskMgr.remove('checkTrickState')
        self.parentNode.removeNode()
        self.startMenuButton.removeNode()
        self.gradeText.removeNode()
        self.scoreText.removeNode()
        self.comboText.removeNode()
        self.timingText.removeNode()
        self.nameText.removeNode()
        self.uiDrawerNode.removeNode()
        base.currPlayer.actor.detach_node()
        self.trickerDummyNode.remove_node()
        self.scene.remove_node()
        base.currPlayer.reset()


