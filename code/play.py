from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.gui.DirectGui import *

from panda3d.core import *

from math import *


class TrickingGame(DirectObject):
    def __init__(self):

        # Load the environment model
        self.parentNode = render.attachNewNode('Play')
        self.scene = loader.loadModel("tp/models/environment")
        self.scene.reparentTo(self.parentNode)

        # Load and transform the actor
        base.tricker.actor.reparent_to(self.parentNode)

        # define controls
        self.accept('d', self.debug)
        self.accept('r', self.reset)
        self.accept('e', self.switchToMainMenu)

        self.accept('shift-y', base.tricker.tryTrick, [base.tricker.gainer, taskMgr])
        self.accept('shift-u', base.tricker.tryTrick, [base.tricker.gswitch, taskMgr])
        self.accept('shift-i', base.tricker.tryTrick, [base.tricker.cork, taskMgr])
        self.accept('shift-o', base.tricker.tryTrick, [base.tricker.doublecork, taskMgr])
        #
        # self.accept('shift-control-y', base.tricker.tryTrick, [base.tricker.flash])
        # self.accept('shift-control-u', base.tricker.tryTrick, [base.tricker.full])
        # self.accept('shift-control-i', base.tricker.tryTrick, [base.tricker.dubfull])
        # self.accept('shift-control-o', base.tricker.tryTrick, [base.tricker.terada])
        #
        # self.accept('control-y', base.tricker.tryTrick, [base.tricker.c540])
        # self.accept('control-u', base.tricker.tryTrick, [base.tricker.c720])
        # self.accept('control-i', base.tricker.tryTrick, [base.tricker.c900])
        # self.accept('control-o', base.tricker.tryTrick, [base.tricker.c1080])
        #
        # self.accept('alt-y', base.tricker.tryTrick, [base.tricker.tdraiz])
        self.accept('alt-u', base.tricker.tryTrick, [base.tricker.btwist, taskMgr])
        # self.accept('alt-i', base.tricker.tryTrick, [base.tricker.snapu])
        # self.accept('alt-o', base.tricker.tryTrick, [base.tricker.cartFull])

        # Add SetCameraTask to task manager
        # IMPORTANT: camera is parented to the dummyNode in tricker's chest
        self.trickerDummyNode = self.parentNode.attach_new_node("trickerDummyNode")
        self.trickerDummyNode.reparentTo(self.parentNode)
        self.trickerDummyNode.setPos(0, 0, 3)

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
        self.uiDrawerNode.reparentTo(render2d)
        self.uiDrawerNode.reparentTo(base.a2dBottomLeftNs)

        self.gradeText = OnscreenText(pos=(-0.2, 0.1), scale=0.3,
                                      parent=base.a2dBottomRight)
        self.scoreText = OnscreenText(pos=(-0.3, -0.2), scale=0.1,
                                      parent=base.a2dTopRight, fg=(1, 1, 1, 1))
        self.comboText = OnscreenText(pos=(0.3, -0.2), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        # DirectButton(text=("OK", "click!", "rolling over", "disabled"))

        taskMgr.add(self.drawUITask, 'drawUI')

    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def drawUITask(self, task):
        grade = base.tricker.getGrade()
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

        scoreStr = "score: " + base.tricker.getScore()
        self.scoreText.setText(scoreStr)

        comboStr = "combo: " + base.tricker.getComboLength()
        self.comboText.setText(comboStr)

        self.uiDrawer.begin()

        # stambar
        sp = base.tricker.stamPercentage()
        self.uiDrawer.rectangleRaw(0.1, 0.1, 1, 0.1, 0, 0, 0, 0, (1, 0, 0, 1))  # red
        self.uiDrawer.rectangleRaw(0.1, 0.1, 1 * sp, 0.1, 0, 0, 0, 0, (0, 1, 0, 1))  # green

        # timingBar
        gp = base.tricker.getTimingBarPercentage()

        self.uiDrawer.rectangleRaw(0.1, 0.3, 1, 0.1, 0, 0, 0, 0, (0, 0, 0, 1))
        self.uiDrawer.rectangleRaw(0.1, 0.3, gp, 0.1, 0, 0, 0, 0, (1, 1, 1, 1))

        self.uiDrawer.end()

        return Task.cont

    def FollowCamTask(self, task):

        # base.disableMouse()
        # self.camera.setPos(self.camera.getPos())

        #  frame = globalClock.getFrameCount()
        #
        # (x, y, z) = base.tricker.actor.getPos()
        # oy = camera.getPos()[1]
        # ox = base.camera.getPos()[0]
        # dy = oy - y
        # error = 20 - dy
        # ny = error/2
        # camera.setPos(ox, ny, 10)
        # # print(list(base.camera.getPos()))
        # # print("oy = %d, ny = %d, error = %d" %(oy, ny, error))
        #  #print(list(base.camera.getPos())[1])
        #
        #  # IMPORTANT: THIS MUST GO AT THE END
        #  base.camera.lookAt(base.trickerDummyNode)
        (ox, oy, oz) = self.trickerDummyNode.getPos()
        (tx, ty, tz) = base.tricker.actor.getPos()
        dx = ox - tx
        dy = oy - ty
        error = 0
        nx = 0 # (dx-error) / 100
        ny = 0
        if dy-error == 0: ny = 0
        else:
            try: ny = log(-dy) / 35
            except: self.trickerDummyNode.setPos((base.tricker.actor), (0,0,3))
        self.trickerDummyNode.setPos(self.trickerDummyNode, (0,ny,0))
        camera.reparentTo(self.trickerDummyNode)
        camera.setPos(-10, -15, 1)
        camera.lookAt(self.trickerDummyNode)

        return Task.cont

    def debug(self):
        print('debug')

    def reset(self):
        taskMgr.remove("follow")
        base.tricker.actor.setPos(0, 0, 0)
        self.trickerDummyNode.setPos(base.tricker.actor, (0,0,3))
        base.tricker.reset()
        self.prevTrick = None

        taskMgr.add(self.FollowCamTask, 'follow')

    def destroy(self):
        self.ignoreAll()
        taskMgr.remove('follow')
        taskMgr.remove('drawUI')
        taskMgr.remove('checkTrickState')
        self.parentNode.removeNode()
        self.gradeText.removeNode()
        self.scoreText.removeNode()
        self.comboText.removeNode()
        self.uiDrawerNode.removeNode()
        base.tricker.actor.detach_node()
        self.trickerDummyNode.remove_node()
        self.scene.remove_node()
