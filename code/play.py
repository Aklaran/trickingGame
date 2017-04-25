from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from tricker import Tricker


from panda3d.core import *

class TrickingGame(object):
    def __init__(self):

        # Load the environment model
        base.scene = base.loader.loadModel("models/environment")
        base.scene.reparentTo(base.render)
        base.scene.setScale(0.25, 0.25, 0.25)
        base.scene.setPos(-8, 42, 0)

        # Load and transform the actor
        self.tricker = Tricker()
        self.tricker.actor.reparent_to(base.render)


        # define controls
        base.accept('d', self.debug)
        base.accept('r', self.reset)
        base.accept('s', self.tricker.save)
        base.accept('l', self.tricker.load)

        base.accept('shift-y', self.tricker.tryTrick,
                    [self.tricker.gainer, base.taskMgr])
        base.accept('shift-u', self.tricker.tryTrick,
                    [self.tricker.gswitch, base.taskMgr])
        # base.accept('shift-i', self.tryTrick, [self.tricker.cork])
        # base.accept('shift-o', self.tryTrick, [self.tricker.dubcork])
        #
        # base.accept('shift-control-y', self.tryTrick, [self.tricker.flash])
        # base.accept('shift-control-u', self.tryTrick, [self.tricker.full])
        # base.accept('shift-control-i', self.tryTrick, [self.tricker.dubfull])
        # base.accept('shift-control-o', self.tryTrick, [self.tricker.terada])
        #
        # base.accept('control-y', self.tryTrick, [self.tricker.c540])
        # base.accept('control-u', self.tryTrick, [self.tricker.c720])
        # base.accept('control-i', self.tryTrick, [self.tricker.c900])
        # base.accept('control-o', self.tryTrick, [self.tricker.c1080])
        #
        # base.accept('alt-y', self.tryTrick, [self.tricker.tdraiz])
        # base.accept('alt-u', self.tryTrick, [self.tricker.btwist])
        # base.accept('alt-i', self.tryTrick, [self.tricker.snapu])
        # base.accept('alt-o', self.tryTrick, [self.tricker.cartFull])

        # Add SetCameraTask to task manager
        # IMPORTANT: camera is parented to the dummyNode in tricker's chest
        self.trickerDummyNode = base.render.attach_new_node("trickerDummyNode")
        self.trickerDummyNode.reparentTo(self.tricker.actor)
        self.trickerDummyNode.setPos(0, 0, 3)

        base.camera.reparentTo(base.render)

        base.taskMgr.add(self.FollowCamTask, "follow")


        # Lights
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        alnp = base.render.attachNewNode(alight)
        base.render.setLight(alnp)

        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        plnp = base.render.attachNewNode(plight)
        plnp.setPos(20, 0, 20)
        base.render.setLight(plnp)

        self.uiDrawer = MeshDrawer2D()
        self.uiDrawer.setBudget(10)
        self.uiDrawerNode = self.uiDrawer.getRoot()
        self.uiDrawerNode.reparentTo(render2d)
        self.uiDrawerNode.reparentTo(base.a2dBottomLeftNs)


        self.gradeText = OnscreenText(pos=(-0.2, 0.1), scale=0.3,
                                      parent=base.a2dBottomRight)
        self.scoreText = OnscreenText(pos=(-0.3, -0.2), scale=0.3,
                                      parent=base.a2dTopRight, fg=(1,1,1,1))
        self.comboText = OnscreenText(pos=(0.2, -0.2), scale=0.3,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        #DirectButton(text=("OK", "click!", "rolling over", "disabled"))

        base.taskMgr.add(self.drawUITask, 'drawUI')


    def drawUITask(self, task):
        gradeStr = self.tricker.getGrade()
        self.gradeText.setText(gradeStr)
        if gradeStr == 'A': self.gradeText.setFg((0,1,0,1))
        elif gradeStr == 'B': self.gradeText.setFg((0.5,1,0,1))
        elif gradeStr == 'C': self.gradeText.setFg((1,1,0,1))
        elif gradeStr == 'D': self.gradeText.setFg((1,0.5,0,1))
        elif gradeStr == 'E': self.gradeText.setFg((1,0,0,1))

        scoreStr = self.tricker.getScore()
        self.scoreText.setText(scoreStr)

        comboStr = self.tricker.getComboLength()
        self.comboText.setText(comboStr)

        self.uiDrawer.begin()

        # stambar
        sp = self.tricker.stamPercentage()
        self.uiDrawer.rectangleRaw(0.1,0.1,1,0.1,0,0,0,0, (1,0,0,1)) #red
        self.uiDrawer.rectangleRaw(0.1,0.1,1*sp,0.1,0,0,0,0, (0,1,0,1)) #green

        #timingBar
        gp = self.tricker.getGreenPercentage()

        self.uiDrawer.rectangleRaw(0.1,0.3,1,0.1, 0,0,0,0, (0,0,0,1))
        self.uiDrawer.rectangleRaw(0.1,0.3,gp, 0.1, 0, 0, 0, 0, (1, 1, 1, 1))

        self.uiDrawer.end()

        return Task.cont

    def FollowCamTask(self, task):

        #self.camera.setPos(self.camera.getPos())

       #  frame = globalClock.getFrameCount()
       #
       #  (x, y, z) = base.tricker.actor.getPos()
       #  #oy = str(list(base.camera.getPos())).split(' ,')[1]
       #  oy = base.camera.getPos()[1]
       #  #oy = camPos[1]
       #  ox = base.camera.getPos()[0]
       #  dy = oy - y
       #  error = 20 - dy
       #  print(error)
       # # print('error:',error)
       #  ny = error/2
       #  base.camera.setPos(base.camera, frame, 1, 20)
       # # print(list(base.camera.getPos()))
       # # print("oy = %d, ny = %d, error = %d" %(oy, ny, error))
       #  #print(list(base.camera.getPos())[1])
       #
       #  # IMPORTANT: THIS MUST GO AT THE END
       #  base.camera.lookAt(base.trickerDummyNode)

        base.camera.reparentTo(self.trickerDummyNode)
        base.camera.setPos(0, -20, 10)
        base.camera.lookAt(self.trickerDummyNode)

        return Task.cont

    def debug(self):
        self.destroy()

    def reset(self):
        self.tricker.actor.setPos(0,0,0)
        self.tricker.reset()