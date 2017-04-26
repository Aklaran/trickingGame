from direct.gui.DirectGui import *

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

        self.nameEntry = None

    def switchToLoad(self):
        base.gameFSM.demand('Load')

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
        if self.nameEntry: self.nameEntry.removeNode()
