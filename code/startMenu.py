from direct.gui.DirectGui import *
from direct.task import Task

from menu import Menu

class StartMenu(Menu):
    def __init__(self):
        super().__init__()

        self.parentNode = aspect2d.attachNewNode('StartMenu')

        self.battleButton = DirectButton(text=("Battle"), scale = 0.15,
                                         command=self.battleNameEntry, parent=self.parentNode,
                                         pos=(0.0, 0, 0))
        self.trainButton = DirectButton(text=("Train"), scale = 0.15,
                                       command=self.openPlayerSelDialog, parent=self.parentNode,
                                        pos=(0,0, -.175))
        self.controlsButton = DirectButton(text='Controls', scale =0.15,
                                           command=self.switchToControls, parent=self.parentNode,
                                           pos=(0.0, 0, -0.350))
        self.statsButton = DirectButton(text=('Stats'), scale=0.15,
                                       command=self.switchToStats, parent=self.parentNode,
                                       pos=(0.0, 0, -0.525))
        self.saveButton = DirectButton(text=('Save'), scale=0.15,
                                       command=self.switchToSave, parent=self.parentNode,
                                       pos=(0.0, 0, -0.7))
        self.loadButton = DirectButton(text=('Load'), scale=0.15,
                                       command=self.switchToLoad, parent=self.parentNode,
                                       pos=(0.0, 0, -0.875))

        self.player1Text = OnscreenText(pos=(0.5, -0.2), scale=0.075,
                                      parent=base.a2dTopLeft)
        self.player2Text = OnscreenText(pos=(-0.5, -0.2), scale=0.075,
                                      parent=base.a2dTopRight)

        self.guiElements = [self.trainButton, self.battleButton, self.saveButton,
                            self.loadButton, self.statsButton, self.controlsButton]

        self.nameEntry = None
        self.playerSelDialog = None

        taskMgr.add(self.drawMenuGraphicsTask, 'drawMenu')

    def openPlayerSelDialog(self):
        self.disableGUI()
        self.playerSelDialog = DirectDialog(dialogName="LoadDialog", scale=1,
                                       text="Who is training?",
                                       buttonTextList=[base.player1.getName(), base.player2.getName()],
                                       buttonValueList=[base.player1,base.player2],
                                       command=self.trainPlayerSel)

    def trainPlayerSel(self, player):
        base.setPlayer(player)
        self.switchToTrain()
        self.playerSelDialog.detachNode()
    def switchToTrain(self):
        if base.currPlayer.hasName():
            self.enableGUI()
            base.gameFSM.demand('Train')
        else:
            self.nameEntry = DirectEntry(text="", scale=0.1, command=self.callSetNameAndDemandTrain,
                                             initialText="Enter Name", focus=1, focusInCommand=self.clearText,
                                             frameSize=(0, 15, 0, 1))
    def battleNameEntry(self):
        self.disableGUI()
        if not base.player1.hasName():
            self.nameEntry = DirectEntry(text="", scale=0.1,
                                         command=self.callSetNameAndDemandBattle, extraArgs=[base.player1, base.player2],
                                         initialText="Enter Name for Player 1", focus=1, focusInCommand=self.clearText,
                                         frameSize=(0, 15, 0, 1))
        elif not base.player2.hasName():
            self.nameEntry = DirectEntry(text="", scale=0.1,
                                         command=self.callSetNameAndDemandBattle, extraArgs=[base.player2,base.player1],
                                         initialText="Enter Name for Player 2", focus=1, focusInCommand=self.clearText,
                                         frameSize=(0, 15, 0, 1))
        else:
            self.enableGUI()
            base.gameFSM.demand('Battle')

    def drawMenuGraphicsTask(self, task):
        player1Str = "Player 1: " + base.player1.getName()
        self.player1Text.setText(player1Str)

        player2Str = "Player 2: " + base.player2.getName()
        self.player2Text.setText(player2Str)

        return Task.cont

    def callSetNameAndDemandTrain(self, textEntered):
        self.enableGUI()
        base.currPlayer.setName(textEntered)
        print(base.currPlayer.saveDict)
        self.nameEntry.detachNode()
        base.gameFSM.demand('Train')

    def callSetNameAndDemandBattle(self, textEntered, player, otherPlayer):
        self.enableGUI()
        player.setName(textEntered)
        self.nameEntry.detachNode()
        if not otherPlayer.hasName():
            self.battleNameEntry()
        else:
            base.gameFSM.demand('Battle')

    def destroy(self):
        self.parentNode.removeNode()
        self.trainButton.removeNode()
        self.saveButton.removeNode()
        self.loadButton.removeNode()
        self.statsButton.removeNode()
        self.player1Text.removeNode()
        self.player2Text.removeNode()
        if self.nameEntry: self.nameEntry.removeNode()

