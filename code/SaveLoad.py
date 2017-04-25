from direct.gui.DirectGui import *

class SaveLoad(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('SaveLoad')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.3,0,-0.3))
        #DirectButton(text=("Save/Load"))
        #DirectButton(text=("My Tricker"))
       # DirectButton(text=("Options"))


    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
