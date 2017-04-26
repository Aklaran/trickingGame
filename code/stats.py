from direct.gui.DirectGui import *

class Stats(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('Stats')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))

        ## Following code block adapted from:
        # https://moguri.github.io/panda-sphinx/programming-with-panda3d/directgui/directscrolledlist.html
        l1 = DirectLabel(text="Test1", text_scale=0.1)
        l2 = DirectLabel(text="Test2", text_scale=0.1)
        l3 = DirectLabel(text="Test3", text_scale=0.1)

        numItemsVisible = 4
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
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
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)
        ## End cited code block

        for fruit in ['apple', 'pear', 'banana', 'orange']:
            l = DirectLabel(text=fruit, text_scale=0.1)
            myScrolledList.addItem(l)

        run()


    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()



