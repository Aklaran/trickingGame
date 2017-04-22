from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *

from tricker import Tricker


from panda3d.core import *


class FollowCam():
    def __init__(self, camera, target):
        self.turnRate = 2.2
        self.camera = camera
        self.target = target

    def updateCameraTask(self, task):
        self.camera.reparentTo(self.target)
        self.camera.setPos(0,-20,10)

class TrickingGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Load and transform the actor
        self.tricker = Tricker()
        self.tricker.actor.reparent_to(self.render)


        # define controls
        self.accept('d', self.debug)
        self.i = 0

        self.accept('shift-y', self.tricker.tryTrick,
                    ['gainer', self.tricker.gainer, self.taskMgr])
        self.accept('shift-u', self.tricker.tryTrick,
                    ['gswitch', self.tricker.gswitch, self.taskMgr])
        # self.accept('shift-i', self.tryTrick, [self.tricker.cork])
        # self.accept('shift-o', self.tryTrick, [self.tricker.dubcork])
        #
        # self.accept('shift-control-y', self.tryTrick, [self.tricker.flash])
        # self.accept('shift-control-u', self.tryTrick, [self.tricker.full])
        # self.accept('shift-control-i', self.tryTrick, [self.tricker.dubfull])
        # self.accept('shift-control-o', self.tryTrick, [self.tricker.terada])
        #
        # self.accept('control-y', self.tryTrick, [self.tricker.c540])
        # self.accept('control-u', self.tryTrick, [self.tricker.c720])
        # self.accept('control-i', self.tryTrick, [self.tricker.c900])
        # self.accept('control-o', self.tryTrick, [self.tricker.c1080])
        #
        # self.accept('alt-y', self.tryTrick, [self.tricker.tdraiz])
        # self.accept('alt-u', self.tryTrick, [self.tricker.btwist])
        # self.accept('alt-i', self.tryTrick, [self.tricker.snapu])
        # self.accept('alt-o', self.tryTrick, [self.tricker.cartFull])

        # Add SetCameraTask to task manager
        # IMPORTANT: camera is parented to the dummyNode in tricker's chest
        self.trickerDummyNode = self.render.attach_new_node("trickerDummyNode")
        self.trickerDummyNode.reparentTo(self.tricker.actor)
        self.trickerDummyNode.setPos(0, 0, 3)

        self.camera.reparentTo(self.render)

        self.taskMgr.add(self.FollowCamTask, "follow")


        # Lights
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(20, 0, 20)
        self.render.setLight(plnp)

    def FollowCamTask(self, task):

        #self.camera.setPos(self.camera.getPos())

       #  frame = globalClock.getFrameCount()
       #
       #  (x, y, z) = self.tricker.actor.getPos()
       #  #oy = str(list(self.camera.getPos())).split(' ,')[1]
       #  oy = self.camera.getPos()[1]
       #  #oy = camPos[1]
       #  ox = self.camera.getPos()[0]
       #  dy = oy - y
       #  error = 20 - dy
       #  print(error)
       # # print('error:',error)
       #  ny = error/2
       #  self.camera.setPos(self.camera, frame, 1, 20)
       # # print(list(self.camera.getPos()))
       # # print("oy = %d, ny = %d, error = %d" %(oy, ny, error))
       #  #print(list(self.camera.getPos())[1])
       #
       #  # IMPORTANT: THIS MUST GO AT THE END
       #  self.camera.lookAt(self.trickerDummyNode)

        self.camera.reparentTo(self.trickerDummyNode)
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(self.trickerDummyNode)

        return Task.cont

    def debug(self):
        print(self.i)
        self.tricker.actor.enableBlend()
        self.tricker.actor.setControlEffect('gainer_bad', self.i)
        self.tricker.actor.setControlEffect('gainer', 1-self.i)
        self.tricker.actor.play('gainer_bad')
        self.tricker.actor.play('gainer')
        self.tricker.actor.disableBlend()

        if self.i == 1:
            self.i = 0
        else:
            self.i = self.i+ 0.5

app = TrickingGame()
app.run()
