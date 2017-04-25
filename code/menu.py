from direct.gui.DirectGui import *

class MainMenu(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('MainMenu')

        self.playButton = DirectButton(text=("Play"), scale = 0.25,
                     command=self.switchToPlay, parent=self.parentNode)
        #DirectButton(text=("Save/Load"))
        #DirectButton(text=("My Tricker"))
       # DirectButton(text=("Options"))


    def switchToPlay(self):
        base.gameFSM.demand('Play')

    def destroy(self):
        self.parentNode.removeNode()
        #self.playButton.destroy()
