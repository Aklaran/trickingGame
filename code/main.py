from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from tricker import Tricker
from tricks import *


from panda3d.core import *


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
        self.taskMgr.add(self.followPlayerTask, "cameraFollowPlayerTask")

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


    def followPlayerTask(self, task):
        # if self.camera.getPos() != (self.tricker.actor.getPos() - (0, 20, 10)):
        x = self.camera.getPos()[0]
        y = self.camera.getPos()[1]
        z = self.camera.getPos()[2]

        dx = (self.tricker.actor.getPos()[0] - x) * .75
        dy = (self.tricker.actor.getPos()[1] - y) * .75
        dz = (self.tricker.actor.getPos()[2] - z)  * .75

        print(dx, dy, dz)

        self.camera.setPos((x+dx, y+dy, z+dz))

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
