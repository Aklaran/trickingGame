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
        #DirectButton(text=("Save/Load"))
        #DirectButton(text=("My Tricker"))
       # DirectButton(text=("Options"))

    def switchToLoad(self):
        base.gameFSM.demand('Load')

    def switchToPlay(self):
        base.gameFSM.demand('Play')

    def switchToSave(self):
        base.gameFSM.demand('Save')

    def destroy(self):
        self.parentNode.removeNode()
        self.playButton.removeNode()
        self.saveButton.removeNode()
