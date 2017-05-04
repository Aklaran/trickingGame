from direct.gui.DirectGui import *

from menu import Menu
import os
import json
from pathlib import Path

class Save(Menu):
    def __init__(self):
        super().__init__()
        self.parentNode = aspect2d.attachNewNode('Save')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))


        # These store dicts that hold saveDict objects of Tricker class
        # for a particular save
        self.slot1ButtonData = self.loadButtonData('1')
        self.slot2ButtonData = self.loadButtonData('2')
        self.slot3ButtonData = self.loadButtonData('3')
        self.slot4ButtonData = self.loadButtonData('4')

        self.slot1Button = DirectButton(text=(self.slot1ButtonData if self.slot1ButtonData else 'Empty Slot 1'),
                                        scale=0.1, pos=(0, 0, .2),
                                        command=self.saveGame, extraArgs=['1'],
                                        parent=self.parentNode)
        self.slot2Button = DirectButton(text=(self.slot2ButtonData if self.slot2ButtonData else 'Empty Slot 2'),
                                        scale=0.1, pos=(0, 0, 0),
                                        command=self.saveGame, extraArgs=['2'],
                                        parent=self.parentNode)
        self.slot3Button = DirectButton(text=(self.slot3ButtonData if self.slot3ButtonData else 'Empty Slot 3'),
                                        scale=0.1, pos=(0, 0, -.2),
                                        command=self.saveGame, extraArgs=['3'],
                                        parent=self.parentNode)
        self.slot4Button = DirectButton(text=(self.slot4ButtonData if self.slot4ButtonData else 'Empty Slot 4'),
                                        scale=0.1, pos=(0, 0, -.4),
                                        command=self.saveGame, extraArgs=['4'],
                                        parent=self.parentNode)

        self.guiElements = [self.slot1Button, self.slot2Button, self.slot3Button, self.slot4Button, self.backButton]

        self.name = ''
        self.nameEntry = None
        self.overwrite = False
        self.overwriteDialog = None
        self.playerSelDialog = None

    def setName(self, textEntered, player, fullFilePath):
        self.enableGUI()
        base.currPlayer.setName(textEntered)
        print(player.saveDict)
        self.nameEntry.detachNode()
        self.existingNameSave(player, fullFilePath)

    def existingNameSave(self, player, fullFilePath):
        with open(fullFilePath, 'w+') as outfile:
            json.dump(player.saveDict, outfile,
                      sort_keys=True, indent=4, ensure_ascii=False)
        self.destroy()
        self.__init__()

    # callback function to set  text
    def itemSel(self, arg, fullFilePath):
        if (arg):
            self.overwrite = True
            self.overwriteDialog.detachNode()
        else:
            self.overwrite = False
            self.enableGUI()
            self.overwriteDialog.detachNode()
        if self.overwrite:
            self.openPlayerSelDialog(fullFilePath)

    def openPlayerSelDialog(self, fullFilePath):
        self.playerSelDialog = DirectDialog(dialogName="playerSelDialog", scale=1,
                                            text="Which player do you want to save?",
                                            buttonTextList=[base.player1.getName(), base.player2.getName()],
                                            buttonValueList=[base.player1, base.player2],
                                            command=self.playerSel, extraArgs=[fullFilePath])
    def playerSel(self, player, fullFilePath):
        if player.hasName():
            self.enableGUI()
            self.playerSelDialog.detachNode()
            self.existingNameSave(player, fullFilePath)
        else:
            self.playerSelDialog.detachNode()
            self.openNameEntry(player, fullFilePath)

    def openNameEntry(self, player, fullFilePath):
        s = "Please enter a name:"
        self.drawPopupText(s)
        self.nameEntry = DirectEntry(text="", scale=0.1, command=self.setName, extraArgs=[player, fullFilePath],
                                     initialText="Shrek", focus=1, focusInCommand=self.clearText,
                                     frameSize=(0, 15, 0, 1), pos=(-0.75,0,0.1))
    def openOverwriteDialog(self, fullFilePath):
        self.overwriteDialog = YesNoDialog(dialogName="OverwriteDialog", scale=1,
                                           text="Do you want to overwrite?", command=self.itemSel,
                                           extraArgs=[fullFilePath])

    def saveGame(self, slot):
        saveFilePath = self.getSaveFilePath(slot)
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        fullFilePathPathwtf = Path(os.path.join(projectPath, saveFilePath))
        print(fullFilePathPathwtf.is_file())
        if fullFilePathPathwtf.is_file():
            self.disableGUI()
            self.openOverwriteDialog(fullFilePath)
        else:
            self.disableGUI()
            self.openPlayerSelDialog(fullFilePath)

    def switchToMainMenu(self):
        base.gameFSM.demand('StartMenu')