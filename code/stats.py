from direct.gui.DirectGui import *

from menu import Menu

class Stats(Menu):
    def __init__(self):
        super().__init__()
        self.parentNode = aspect2d.attachNewNode('Stats')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))

        ## Following code block adapted from:
        # https://moguri.github.io/panda-sphinx/programming-with-panda3d/directgui/directscrolledlist.html
        numItemsVisible = 4
        itemHeight = 0.11

        self.statsList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Dec",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Inc",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(1, 0, 0, 0.5),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
            parent=self.parentNode
        )

        skillDict = base.currPlayer.getSkillDict()
        for trick in skillDict:
            s = str(trick + ": " + str(int(skillDict[trick])))
            l = DirectLabel(text=s, text_scale=0.1)
            self.statsList.addItem(l)
        ## End cited code block

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
        self.statsList.removeNode()



