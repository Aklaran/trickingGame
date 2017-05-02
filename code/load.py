from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait

from menu import Menu
import os
import json
from pathlib import Path

class Load(Menu):
    def __init__(self):
        super().__init__()
        self.parentNode = aspect2d.attachNewNode('Load')

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
                                        command=self.openLoadDialog, extraArgs=['1'],
                                        parent=self.parentNode)
        self.slot2Button = DirectButton(text=(self.slot2ButtonData if self.slot2ButtonData else 'Empty Slot 2'),
                                        scale=0.1, pos=(0, 0, 0),
                                        command=self.openLoadDialog, extraArgs=['2'],
                                        parent=self.parentNode)
        self.slot3Button = DirectButton(text=(self.slot3ButtonData if self.slot3ButtonData else 'Empty Slot 3'),
                                        scale=0.1, pos=(0, 0, -.2),
                                        command=self.openLoadDialog, extraArgs=['3'],
                                        parent=self.parentNode)
        self.slot4Button = DirectButton(text=(self.slot4ButtonData if self.slot4ButtonData else 'Empty Slot 4'),
                                        scale=0.1, pos=(0, 0, -.4),
                                        command=self.openLoadDialog, extraArgs=['4'],
                                        parent=self.parentNode)

        self.loadDialog = None

    @staticmethod
    def getSaveFilePath(slot):
        if os.name == 'nt':
            return 'saves\save' + slot + '.json'
        else:
            return 'saves/save' + slot + '.json'

    def openLoadDialog(self, slot):
        saveFilePath = self.getSaveFilePath(slot)
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        fullFilePathPathwtf = Path(os.path.join(projectPath, saveFilePath))
        if fullFilePathPathwtf.is_file():
            self.loadDialog = DirectDialog(dialogName="LoadDialog", scale=1,
                                           text="Which player do do you want to load to?",
                                           buttonTextList=['Player 1', 'Player 2'],
                                           buttonValueList=[base.player1,base.player2],
                                           command=self.loadGame, extraArgs=[fullFilePath])
        else:
            s = "Save not found!"
            self.drawPopupText(s)

    def loadGame(self, player, fullFilePath):
        print("old:", player.saveDict)
        with open(fullFilePath, 'r') as infile:
            player.loadToSaveDict(json.load(infile))
            s = "Loaded file... " + player.name
            self.drawPopupText(s)
            print("player1: ", base.player1.saveDict)
            print("player2: ", base.player2.saveDict)
        self.loadDialog.detachNode()