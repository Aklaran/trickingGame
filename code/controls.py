from menu import Menu
from direct.gui.DirectGui import *

class Controls(Menu):
    def __init__(self):
        super().__init__()
        self.parentNode = aspect2d.attachNewNode('Save')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))

        self.background = OnscreenImage(parent=render2dp, image='tp/images/controls.png')
        base.cam2dp.node().getDisplayRegion(0).setSort(-20)