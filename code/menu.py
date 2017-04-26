from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait

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

        self.nameEntry = None
        self.popupText = None
        self.popupSeq = None

    def switchToStats(self):
        if base.tricker.hasName():
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
        base.tricker.setName(textEntered)
        print(base.tricker.saveDict)
        self.nameEntry.detachNode()
        base.gameFSM.demand('Play')

    def switchToPlay(self):
        if base.tricker.hasName():
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
        if self.nameEntry: self.nameEntry.removeNode()
