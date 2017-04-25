from direct.gui.DirectGui import *

import os
import json
from pathlib import Path

class Save(object):
    def __init__(self):
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

        self.name = ''
        self.nameEntry = None
        self.overwrite = False

    def callSetName(self, textEntered):
        base.tricker.setName(textEntered)
        self.name = textEntered


    def clearText(self):
        self.nameEntry.enterText('')

    # callback function to set  text
    def itemSel(self, arg):
        if (arg):
            output = "Button Selected is: Yes"
            self.overwrite = True
        else:
            self.overwrite = False


    def saveGame(self, slot):
        saveFilePath = 'saves/save' + slot + '.json'
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        fullFilePathPathwtf = Path(os.path.join(projectPath, saveFilePath))
        if fullFilePathPathwtf.is_file():
            overwriteDialog = YesNoDialog(dialogName="OverwriteDialog", scale=1,
                                               text="Do you want to overwrite?", command=self.itemSel)
            if self.overwrite:
                if base.tricker.name == '':
                    self.nameEntry = DirectEntry(text="", scale=0.1, command=self.callSetName,
                                                initialText="Shrek",focus=1,focusInCommand=self.clearText,
                                                frameSize = (0,15,0,1))
                with open(fullFilePath, 'w+') as outfile:
                    json.dump(base.tricker.saveDict, outfile,
                              sort_keys=True, indent=4, ensure_ascii=False)


    def loadButtonData(self, slot):
        saveFilePath = 'saves/save' + slot + '.json'
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        fullFilePathPathwtf = Path(os.path.join(projectPath, saveFilePath))
        if fullFilePathPathwtf.is_file():
            with open(fullFilePath, 'r') as infile:
                saveDict = json.load(infile)
                name = saveDict['name']
                level = saveDict['level']
                return name + "   lv" + str(level)
        print("Save not found!")

    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
        self.slot1Button.removeNode()
        self.slot2Button.removeNode()
        self.slot3Button.removeNode()
        self.slot4Button.removeNode()
        if self.nameEntry: self.nameEntry.removeNode()
