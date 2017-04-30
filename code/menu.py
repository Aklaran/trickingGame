from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.task import Task

class MainMenu(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('MainMenu')

        self.playButton = DirectButton(text=("Play"), scale = 0.25,
                                       command=self.switchToPlay, parent=self.parentNode)
        self.saveButton = DirectButton(text=('Save'), scale=0.25,
                                       command=self.switchToSave, parent=self.parentNode,
                                       pos=(0.0, 0, -0.325))
        self.loadButton = DirectButton(text=('Load'), scale=0.25,
                                       command=self.switchToLoad, parent=self.parentNode,
                                       pos=(0.0, 0, -0.6))
        self.statsButton = DirectButton(text=('Stats'), scale=0.25,
                                       command=self.switchToStats, parent=self.parentNode,
                                       pos=(0.0, 0, -0.875))

        self.player1Text = OnscreenText(pos=(0.5, -0.2), scale=0.075,
                                      parent=base.a2dTopLeft)
        self.player2Text = OnscreenText(pos=(-0.5, -0.2), scale=0.075,
                                      parent=base.a2dTopRight)

        self.nameEntry = None
        self.popupText = None
        self.popupSeq = None

        taskMgr.add(self.drawMenuGraphicsTask, 'drawMenu')

    def drawMenuGraphicsTask(self, task):
        player1Str = "Player 1: " + base.player1.getName()
        self.player1Text.setText(player1Str)

        player2Str = "Player 2: " + base.player2.getName()
        self.player2Text.setText(player2Str)

        return Task.cont

    def switchToStats(self):
        if base.currPlayer.hasName():
            base.gameFSM.demand('Stats')
        else:
            s = 'No save data found. Press Play to make a character!'
            self.drawPopupText(s)

    def switchToLoad(self):
        base.gameFSM.demand('Load')

    def createPopupText(self,s):
        self.popupText = OnscreenText(text=s, scale = 0.07, parent=base.a2dTopCenter,
                                      pos = (0,-.05) )

    def removePopupText(self):
        self.popupText.detachNode()
        self.popupText = None
        self.popupSeq = None

    def drawPopupText(self, s):
        if not self.popupSeq:
            self.popupSeq = Sequence(Func(self.createPopupText, s),
                     Wait(1.5),
                     Func(self.removePopupText))
            self.popupSeq.start()

    def clearText(self):
        self.nameEntry.enterText('')

    def callSetNameAndDemandPlay(self, textEntered):
        base.currPlayer.setName(textEntered)
        print(base.currPlayer.saveDict)
        self.nameEntry.detachNode()
        base.gameFSM.demand('Play')

    def switchToPlay(self):
        if base.currPlayer.hasName():
            base.gameFSM.demand('Play')
        else:
            self.nameEntry = DirectEntry(text="", scale=0.1, command=self.callSetNameAndDemandPlay,
                                             initialText="Enter Name", focus=1, focusInCommand=self.clearText,
                                             frameSize=(0, 15, 0, 1))

    def switchToSave(self):
        base.gameFSM.demand('Save')

    def destroy(self):
        self.parentNode.removeNode()
        self.playButton.removeNode()
        self.saveButton.removeNode()
        self.loadButton.removeNode()
        self.statsButton.removeNode()
        self.player1Text.removeNode()
        self.player2Text.removeNode()
        if self.nameEntry: self.nameEntry.removeNode()

