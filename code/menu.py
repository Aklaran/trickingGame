from direct.gui.DirectGui import *

class MainMenu(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('MainMenu')

        self.playButton = DirectButton(text=("Play"), scale = 0.25,
                     command=self.switchToPlay, parent=self.parentNode)
        self.saveLoadButton = DirectButton(text=('Save/Load'), scale=0.25,
                                           command=self.switchToSaveLoad, parent=self.parentNode,
                                           pos=(0.0, 0, -0.5))
        #DirectButton(text=("Save/Load"))
        #DirectButton(text=("My Tricker"))
       # DirectButton(text=("Options"))

    def switchToPlay(self):
        base.gameFSM.demand('Play')

    def switchToSaveLoad(self):
        base.gameFSM.demand('SaveLoad')

    def destroy(self):
        self.parentNode.removeNode()
        self.playButton.removeNode()
