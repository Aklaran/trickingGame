from direct.gui.DirectGui import *

from menu import Menu

class Stats(Menu):
    def __init__(self):
        super().__init__()
        self.parentNode = aspect2d.attachNewNode('Stats')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))

        self.p1StatsList = None
        self.p2StatsList = None
        
        if base.player1.hasName():
            self.p1StatsList = self.createStatsList(base.player1)
        if base.player2.hasName():
            self.p2StatsList = self.createStatsList(base.player2)
            
    def createStatsList(self, player):
        ## Following code block adapted from:
        # https://moguri.github.io/panda-sphinx/programming-with-panda3d/directgui/directscrolledlist.html
        numItemsVisible = 8
        itemHeight = 0.11

        if player == base.player1: listPos = (-1,0,0)
        elif player == base.player2: listPos = (0.25,0,0)
        
        statsList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Dec",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Inc",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.40, 0.59),
            frameColor=(0.5, 0.5, 0.5, 0.5),
            pos=listPos,
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.3, 0.3, -0.70, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
            parent=self.parentNode
        )

        nameAndLevel = player.getName() + " : lv" + player.getLevel()
        nameLabel = DirectLabel(text=nameAndLevel,text_scale=0.1)
        statsList.addItem(nameLabel)
        stamLabel = DirectLabel(text=("stamina : " + player.getTotalStam()), text_scale=0.1)
        statsList.addItem(stamLabel)
        skillDict = player.getSkillDict()
        for trick in skillDict:
            s = str(trick + ": " + str(int(skillDict[trick])))
            l = DirectLabel(text=s, text_scale=0.1)
            statsList.addItem(l)
        ## End cited code block

        return statsList

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
        if self.p1StatsList: self.p1StatsList.removeNode()
        if self.p2StatsList: self.p2StatsList.removeNode()



