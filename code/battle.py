from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.gui.DirectGui import *

from panda3d.core import *

from math import *

from battleData import BattleData


class BattleMode(DirectObject):
    def __init__(self):

        self.battleData = BattleData()

        # Load the environment model
        self.parentNode = render.attachNewNode('BattleMode')
        self.scene = loader.loadModel("tp/models/environment")
        self.scene.reparentTo(self.parentNode)

        # Load the actor
        base.currPlayer.actor.reparentTo(self.parentNode)
        base.currPlayer.actor.setPos(0,0,0)
        base.currPlayer.actor.pose('btwist', 1)

        # define controls
        self.accept('d', self.debug)
        self.accept('e', self.switchToMainMenu)

        self.accept('shift-y', base.currPlayer.tryTrick, [base.currPlayer.gainer, taskMgr])
        self.accept('shift-u', base.currPlayer.tryTrick, [base.currPlayer.gswitch, taskMgr])
        self.accept('shift-i', base.currPlayer.tryTrick, [base.currPlayer.cork, taskMgr])
        self.accept('shift-o', base.currPlayer.tryTrick, [base.currPlayer.doublecork, taskMgr])
        #
        # self.accept('shift-control-y', base.currPlayer.tryTrick, [base.currPlayer.flash])
        # self.accept('shift-control-u', base.currPlayer.tryTrick, [base.currPlayer.full])
        # self.accept('shift-control-i', base.currPlayer.tryTrick, [base.currPlayer.dubfull])
        # self.accept('shift-control-o', base.currPlayer.tryTrick, [base.currPlayer.terada])
        #
        # self.accept('control-y', base.currPlayer.tryTrick, [base.currPlayer.c540])
        # self.accept('control-u', base.currPlayer.tryTrick, [base.currPlayer.c720])
        # self.accept('control-i', base.currPlayer.tryTrick, [base.currPlayer.c900])
        # self.accept('control-o', base.currPlayer.tryTrick, [base.currPlayer.c1080])
        #
        # self.accept('alt-y', base.currPlayer.tryTrick, [base.currPlayer.tdraiz])
        self.accept('alt-u', base.currPlayer.tryTrick, [base.currPlayer.btwist, taskMgr])
        # self.accept('alt-i', base.currPlayer.tryTrick, [base.currPlayer.snapu])
        # self.accept('alt-o', base.currPlayer.tryTrick, [base.currPlayer.cartFull])

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

        self.gradeText  = OnscreenText(pos=(-0.4, -0.3), scale=0.3,
                                      parent=base.a2dTopRight)
        self.timingText = OnscreenText(pos=(-0.5, -0.5), scale = 0.075,
                                       parent=base.a2dTopRight, fg=(1, 1, 1, 1))
        self.scoreText  = OnscreenText(pos=(0.3, -0.3), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.oppScoreText  = OnscreenText(pos=(0.5, -0.4), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.comboText  = OnscreenText(pos=(0.3, -0.2), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.nameText   = OnscreenText(text=base.currPlayer.getName(),
                                       pos=(0, -0.2), scale = 0.1,
                                       parent = base.a2dTopCenter, fg=(1,1,1,1))
        self.p1RoundText = OnscreenText(pos=(0.3, 0.2), scale = 0.1,
                                        parent = base.a2dBottomLeft, fg=(1,1,1,1))
        self.p2RoundText = OnscreenText(pos=(-0.3, 0.2), scale=0.1,
                                        parent=base.a2dBottomRight, fg=(1, 1, 1, 1))

        self.endGameDialog = None

        taskMgr.add(self.drawUITask, 'drawUI')

        taskMgr.add(self.checkGameStateTask, 'checkGameState')

    def switchToMainMenu(self):
        base.gameFSM.demand('StartMenu')

    def drawUITask(self, task):
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

        p1RoundStr = base.player1.getName() + "\n" + str(self.battleData.getRounds(1))
        p2RoundStr = base.player2.getName() + "\n" + str(self.battleData.getRounds(2))
        self.p1RoundText.setText(p1RoundStr)
        self.p2RoundText.setText(p2RoundStr)


        scoreStr = "score: " + base.currPlayer.getScore()
        self.scoreText.setText(scoreStr)

        oppScoreStr = "score to beat: " + str(self.battleData.getOppScore())
        self.oppScoreText.setText(oppScoreStr)

        comboStr = "combo: " + base.currPlayer.getComboLength()
        self.comboText.setText(comboStr)

        timingStr = "timing: " + base.currPlayer.getTiming()
        self.timingText.setText(timingStr)

        self.uiDrawer.begin()
        timingWidth = 1.5
        stamWidth = 1

        # stambar
        sp = base.currPlayer.stamPercentage()
        self.uiDrawer.rectangleRaw(-timingWidth/2, 0.15, stamWidth, 0.1, 0, 0, 0, 0, (1, 0, 0, 1))  # red
        self.uiDrawer.rectangleRaw(-timingWidth/2, 0.15, stamWidth * sp, 0.1, 0, 0, 0, 0, (0, 1, 0, 1))  # green

        # timingBar
        gp = base.currPlayer.getTimingBarPercentage()

        self.uiDrawer.rectangleRaw(-timingWidth/2, 0.25, timingWidth, 0.1, 0, 0, 0, 0, (0, 0, 0, 1))
        self.uiDrawer.rectangleRaw(-timingWidth/2, 0.25, gp*timingWidth, 0.1, 0, 0, 0, 0, (1, 1, 1, 1))

        self.uiDrawer.end()

        return Task.cont

    def checkGameStateTask(self, task):
        if base.currPlayer.comboHasEnded():
            self.ignoreAll()
            taskMgr.doMethodLater(2, self.changeTurnTask, 'changeTurn',
                                  extraArgs=[base.currPlayer, False], appendTask=True)
            return Task.done
        elif base.currPlayer.isFalling():
            self.ignoreAll()
            taskMgr.doMethodLater(4, self.changeTurnTask, 'changeTurn',
                                  extraArgs=[base.currPlayer, True], appendTask=True)
            return Task.done
        return Task.cont

    def changeTurnTask(self, currPlayer, falling, task):
        self.battleData.updateScore(currPlayer, int(currPlayer.getScore()), falling)
        currPlayer.reset()
        self.battleData.checkEndRound()
        winner = self.battleData.checkEndGame()
        if winner:
            taskMgr.doMethodLater(1, self.showEndGameDialogTask, 'EndGameDialog', extraArgs=[winner], appendTask=True)
            return Task.done
        if currPlayer == base.player1:
            base.setPlayer(base.player2)
        elif currPlayer == base.player2:
            base.setPlayer(base.player1)
        self.reset()
        return Task.done

    def showEndGameDialogTask(self, winner, taskMgr):
        endGameStr = winner.getName() + " wins!"
        self.endGameDialog = DirectDialog(dialogName="endGameDialog", scale=1,
                                       text=endGameStr,
                                       buttonTextList=['Quit', 'Rematch'],
                                       buttonValueList=['quit', 'rematch'],
                                       command=self.endGameItemSel)
    def endGameItemSel(self, arg):
        if arg == 'quit':
            self.switchToMainMenu()
        elif arg == 'rematch':
            self.battleData.__init__()
            base.currPlayer = base.player1
            self.reset()

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

    def debug(self):
        print('debug')

    def reset(self):
        # taskMgr.remove("follow")
        # base.currPlayer.actor.setPos(0, 0, 0)
        # self.trickerDummyNode.setPos(base.currPlayer.actor, (0,0,3))
        # self.nameText.setText(base.currPlayer.getName())
        self.ignoreAll()
        base.currPlayer.actor.detachNode()
        base.currPlayer.actor.reparentTo(self.parentNode)
        base.currPlayer.reset()
        self.destroy()
        self.reInit()

    def destroy(self):
        self.ignoreAll()
        taskMgr.remove('follow')
        taskMgr.remove('drawUI')
        taskMgr.remove('checkTrickState')
        self.parentNode.removeNode()
        self.gradeText.removeNode()
        self.scoreText.removeNode()
        self.oppScoreText.removeNode()
        self.comboText.removeNode()
        self.timingText.removeNode()
        self.nameText.removeNode()
        self.p1RoundText.removeNode()
        self.p2RoundText.removeNode()
        self.uiDrawerNode.removeNode()
        base.currPlayer.actor.detach_node()
        self.trickerDummyNode.removeNode()
        self.scene.detachNode()
        if self.endGameDialog: self.endGameDialog.detachNode()

    def reInit(self):

        # Load the environment model
        self.parentNode = render.attachNewNode('BattleMode')
        self.scene = loader.loadModel("tp/models/environment")
        self.scene.reparentTo(self.parentNode)

        # Load the actor
        base.currPlayer.actor.reparentTo(self.parentNode)
        base.currPlayer.actor.setPos(0,0,0)
        base.currPlayer.actor.pose('btwist', 1)

        # define controls
        self.accept('d', self.debug)
        self.accept('e', self.switchToMainMenu)

        self.accept('shift-y', base.currPlayer.tryTrick, [base.currPlayer.gainer, taskMgr])
        self.accept('shift-u', base.currPlayer.tryTrick, [base.currPlayer.gswitch, taskMgr])
        self.accept('shift-i', base.currPlayer.tryTrick, [base.currPlayer.cork, taskMgr])
        self.accept('shift-o', base.currPlayer.tryTrick, [base.currPlayer.doublecork, taskMgr])
        #
        # self.accept('shift-control-y', base.currPlayer.tryTrick, [base.currPlayer.flash])
        # self.accept('shift-control-u', base.currPlayer.tryTrick, [base.currPlayer.full])
        # self.accept('shift-control-i', base.currPlayer.tryTrick, [base.currPlayer.dubfull])
        # self.accept('shift-control-o', base.currPlayer.tryTrick, [base.currPlayer.terada])
        #
        # self.accept('control-y', base.currPlayer.tryTrick, [base.currPlayer.c540])
        # self.accept('control-u', base.currPlayer.tryTrick, [base.currPlayer.c720])
        # self.accept('control-i', base.currPlayer.tryTrick, [base.currPlayer.c900])
        # self.accept('control-o', base.currPlayer.tryTrick, [base.currPlayer.c1080])
        #
        # self.accept('alt-y', base.currPlayer.tryTrick, [base.currPlayer.tdraiz])
        self.accept('alt-u', base.currPlayer.tryTrick, [base.currPlayer.btwist, taskMgr])
        # self.accept('alt-i', base.currPlayer.tryTrick, [base.currPlayer.snapu])
        # self.accept('alt-o', base.currPlayer.tryTrick, [base.currPlayer.cartFull])

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

        self.gradeText  = OnscreenText(pos=(-0.4, -0.3), scale=0.3,
                                      parent=base.a2dTopRight)
        self.timingText = OnscreenText(pos=(-0.5, -0.5), scale = 0.075,
                                       parent=base.a2dTopRight, fg=(1, 1, 1, 1))
        self.scoreText  = OnscreenText(pos=(0.3, -0.3), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.oppScoreText  = OnscreenText(pos=(0.5, -0.4), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.comboText  = OnscreenText(pos=(0.3, -0.2), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.nameText   = OnscreenText(text=base.currPlayer.getName(),
                                       pos=(0, -0.2), scale = 0.1,
                                       parent = base.a2dTopCenter, fg=(1,1,1,1))
        self.p1RoundText = OnscreenText(pos=(0.3, 0.2), scale = 0.1,
                                        parent = base.a2dBottomLeft, fg=(1,1,1,1))
        self.p2RoundText = OnscreenText(pos=(-0.3, 0.2), scale=0.1,
                                        parent=base.a2dBottomRight, fg=(1, 1, 1, 1))

        self.endGameDialog = None

        taskMgr.add(self.drawUITask, 'drawUI')

        taskMgr.add(self.checkGameStateTask, 'checkGameState')
