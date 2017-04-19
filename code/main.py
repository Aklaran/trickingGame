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

        #Load tricks
        gainer = Gainer()
        gswitch = Gswitch()

        # define controls
        self.accept('d', self.debug)

        self.accept('shift-y', self.tryTrick, ['gainer', gainer])
        self.accept('shift-u', self.tryTrick, ['gswitch', gswitch])
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
        self.camera.reparentTo(self.tricker.actor)
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


        # TODO: find a better place to put this variable lol
        self.prevTrick = None

    def followPlayerTask(self, task):
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(self.tricker.actor)
        return Task.cont

    def debug(self, prevInterval):
        print(prevInterval)

    def tryTrick(self, animation, trick):
        currAnim = self.tricker.actor.getCurrentAnim()
        if currAnim:
            if self.prevTrick.getExitTransition() != trick.getEntryTransition():
                print("invalid transition")
                return
            currFrame = self.tricker.actor.getCurrentFrame(currAnim)
            numFrames = self.tricker.actor.getNumFrames(currAnim)
            framesLeft = numFrames - currFrame

            grade = self.prevTrick.getGrade(currFrame)
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
                return

            # 0.06 is the time it takes for 2 frames - smooth blending
            delayTime = framesLeft / 30 - 0.06
            self.taskMgr.doMethodLater(delayTime, self.doTrickTask, 'doTrick',
                             extraArgs=[animation], appendTask=True)
        else:
            self.taskMgr.add(self.doTrickTask, 'doTrick',
                             extraArgs=[animation], appendTask=True)
        self.prevTrick = trick

    def doTrickTask(self, animation, task):
        airTime = self.tricker.actor.getNumFrames(animation) / 30
        moveInterval = self.tricker.actor.posInterval(airTime,
                                                Point3(0, .1, 0),
                                                other=self.tricker.actor)
        self.tricker.actor.play(animation)

        moveInterval.start()
        return Task.done



app = TrickingGame()
app.run()
