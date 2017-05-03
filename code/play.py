from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.task import Task
from direct.gui.DirectGui import *

from panda3d.core import *

from math import *

class Play(DirectObject):
    def __init__(self):
        # Load the environment model
        self.parentNode = render.attachNewNode('BattleMode')
        self.scene = loader.loadModel("tp/models/environment")
        self.scene.reparentTo(self.parentNode)

        # Load the actor
        base.currPlayer.actor.reparentTo(self.parentNode)
        base.currPlayer.actor.setPos(0, 0, 0)
        base.currPlayer.actor.pose('btwist', 1)

        # define controls
        self.accept('shift-u', base.currPlayer.tryTrick, [base.currPlayer.gainer, taskMgr])
        self.accept('shift-i', base.currPlayer.tryTrick, [base.currPlayer.gswitch, taskMgr])
        self.accept('shift-o', base.currPlayer.tryTrick, [base.currPlayer.cork, taskMgr])
        self.accept('shift-p', base.currPlayer.tryTrick, [base.currPlayer.doublecork, taskMgr])

        # self.accept('control-u', base.currPlayer.tryTrick, [base.currPlayer.c540])
        self.accept('control-i', base.currPlayer.tryTrick, [base.currPlayer.btwist, taskMgr])
        # self.accept('control-o', base.currPlayer.tryTrick, [base.currPlayer.]][]  raiz])
        # self.accept('control-p', base.currPlayer.tryTrick, [base.currPlayer.cartFull])

        # Add SetCameraTask to task manager
        # IMPORTANT: camera is parented to the dummyNode in tricker's chest
        self.trickerDummyNode = self.parentNode.attach_new_node("trickerDummyNode")
        self.trickerDummyNode.reparentTo(self.parentNode)
        self.trickerDummyNode.setPos(base.currPlayer.actor, (0, 0, 3))

        camera.reparentTo(self.parentNode)

        camera.setPos(0, -20, 10)
        camera.lookAt(self.trickerDummyNode)

        taskMgr.add(self.FollowCamTask, "follow")

        # Lights
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        alnp = self.parentNode.attachNewNode(alight)
        self.parentNode.setLight(alnp)

        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        plnp = self.parentNode.attachNewNode(plight)
        plnp.setPos(20, 0, 20)
        self.parentNode.setLight(plnp)

        self.uiDrawer = MeshDrawer2D()
        self.uiDrawer.setBudget(10)
        self.uiDrawerNode = self.uiDrawer.getRoot()
        self.uiDrawerNode.reparentTo(base.a2dBottomCenter)

        self.gradeText = OnscreenText(pos=(-0.4, -0.3), scale=0.3,
                                      parent=base.a2dTopRight)
        self.timingText = OnscreenText(pos=(-0.5, -0.5), scale=0.075,
                                       parent=base.a2dTopRight, fg=(1, 1, 1, 1))
        self.scoreText = OnscreenText(pos=(0.3, -0.3), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.comboText = OnscreenText(pos=(0.3, -0.2), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.nameText = OnscreenText(text=base.currPlayer.getName(),
                                     pos=(0, -0.2), scale=0.2,
                                     parent=base.a2dTopCenter, fg=(1, 1, 1, 1))
        self.stamBarText = OnscreenText(text="stamina", scale=0.075,
                                        parent=base.a2dBottomCenter, pos=(-0.6,0.09),
                                        fg=(1,1,1,1))
        self.timeBarText = OnscreenText(text="timing", scale=0.075,
                                        parent=base.a2dBottomCenter, pos=(-0.625, 0.375),
                                        fg=(1, 1, 1, 1))

        self.startMenuButton = DirectButton(text=("quit"), scale=0.075,
                                            command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                            pos=(0.075, 0, -0.07))

        self.initialDialog = None
        self.popupText = None
        self.popupSeq = None

    def switchToMainMenu(self):
        base.gameFSM.demand('StartMenu')

    def drawUITask(self, mode, task):
        grade = base.currPlayer.getGrade()
        if grade == 0:
            self.gradeText.setText('A')
            self.gradeText.setFg((0, 1, 0, 1))
        elif grade == 1:
            self.gradeText.setText('B')
            self.gradeText.setFg((0.5, 1, 0, 1))
        elif grade == 2:
            self.gradeText.setText('C')
            self.gradeText.setFg((1, 1, 0, 1))
        elif grade == 3:
            self.gradeText.setText('D')
            self.gradeText.setFg((1, 0.5, 0, 1))
        elif grade == 4:
            self.gradeText.setText('F')
            self.gradeText.setFg((1, 0, 0, 1))

        scoreStr = "score: " + base.currPlayer.getScore()
        self.scoreText.setText(scoreStr)

        comboStr = "combo: " + base.currPlayer.getComboLength()
        self.comboText.setText(comboStr)

        if base.currPlayer.getTiming(): timingStr = "timing: " + base.currPlayer.getTiming()
        else: timingStr = ""
        self.timingText.setText(timingStr)

        if mode == 'battle':
            p1RoundStr = base.player1.getName() + "\n" + str(self.battleData.getRounds(1))
            p2RoundStr = base.player2.getName() + "\n" + str(self.battleData.getRounds(2))
            self.p1RoundText.setText(p1RoundStr)
            self.p2RoundText.setText(p2RoundStr)

            oppScoreStr = "score to beat: " + str(self.battleData.getOppScore())
            self.oppScoreText.setText(oppScoreStr)

        self.uiDrawer.begin()
        timingWidth = 1.5
        stamWidth = 1

        # stambar
        sp = base.currPlayer.stamPercentage()
        self.uiDrawer.rectangleRaw(-timingWidth / 2, 0.15, stamWidth, 0.1, 0, 0, 0, 0,
                                   (0.831081081, 0.33783783783, 1, 1))  # red
        self.uiDrawer.rectangleRaw(-timingWidth / 2, 0.15, stamWidth * sp, 0.1, 0, 0, 0, 0,
                                   (0, 1, 0.4044117647, 1))  # green

        # timingBar
        gp = base.currPlayer.getTimingBarPercentage()

        self.uiDrawer.rectangleRaw(-timingWidth / 2, 0.25, timingWidth, 0.1, 0, 0, 0, 0, (0, 0, 0, 1))
        self.uiDrawer.rectangleRaw(-timingWidth / 2, 0.25, timingWidth * gp, 0.1, 0, 0, 0, 0, (1, 1, 1, 1))

        self.uiDrawer.end()

        return Task.cont

    def FollowCamTask(self, task):
        (ox, oy, oz) = self.trickerDummyNode.getPos()
        (tx, ty, tz) = base.currPlayer.actor.getPos()
        dx = ox - tx
        dy = oy - ty
        error = 0
        nx = 0 # (dx-error) / 100
        ny = 0
        if dy-error == 0: ny = 0
        else:
            try: ny = log(-dy) / 15
            except: self.trickerDummyNode.setPos((base.currPlayer.actor), (0,0,3))
        self.trickerDummyNode.setPos(self.trickerDummyNode, (0,ny,0))
        camera.reparentTo(self.trickerDummyNode)
        camera.setPos(-10, -15, 1)
        camera.lookAt(self.trickerDummyNode)

        return Task.cont

    def createPopupText(self,s):
        self.popupText = OnscreenText(text=s, scale = 0.07, parent=render2d,
                                      pos = (0,0.4) )

    def removePopupText(self):
        self.popupText.detachNode()
        self.popupText = None
        self.popupSeq = None

    def drawPopupText(self, s):
        if not self.popupSeq:
            self.popupSeq = Sequence(Func(self.createPopupText, s),
                     Wait(2),
                     Func(self.removePopupText))
            self.popupSeq.start()

    def destroy(self):
        self.ignoreAll()
        taskMgr.remove('follow')
        taskMgr.remove('drawUI')
        taskMgr.remove('checkTrickState')
        taskMgr.remove('checkGameState')
        taskMgr.remove('reset')
        self.parentNode.removeNode()
        self.startMenuButton.removeNode()
        self.gradeText.removeNode()
        self.scoreText.removeNode()
        self.comboText.removeNode()
        self.timingText.removeNode()
        self.nameText.removeNode()
        self.stamBarText.removeNode()
        self.timeBarText.removeNode()
        self.uiDrawerNode.removeNode()
        base.currPlayer.actor.detach_node()
        self.trickerDummyNode.remove_node()
        self.scene.remove_node()
        base.currPlayer.reset()