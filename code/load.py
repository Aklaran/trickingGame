from direct.gui.DirectGui import *

class Load(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('Load')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))
        #DirectButton(text=("Save/Load"))
        #DirectButton(text=("My Tricker"))
        #DirectButton(text=("Options"))


    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
