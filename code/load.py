from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait

import os
import json
from pathlib import Path

class Load(object):
    def __init__(self):
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

        self.popupText = None
        self.popupSeq = None
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

    def loadButtonData(self, slot):
        saveFilePath = self.getSaveFilePath(slot)
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        fullFilePathPathwtf = Path(os.path.join(projectPath, saveFilePath))
        if fullFilePathPathwtf.is_file():
            with open(fullFilePath, 'r') as infile:
                saveDict = json.load(infile)
                name = saveDict['name']
                level = saveDict['level']
                return name + "   lv" + str(level)

    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def createPopupText(self,s):
        self.popupText = OnscreenText(text=s, scale = 0.07, parent=base.a2dBottomCenter,
                                      pos = (0,.05) )

    def removePopupText(self):
        self.popupText.detachNode()
        self.popupText = None
        self.popupSeq = None

    def drawPopupText(self, s):
        if not self.popupSeq:
            self.popupSeq = Sequence(Func(self.createPopupText, s),
                     Wait(1.5),
                     Func(self.removePopupText))
            self.popupSeq.start()

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
        self.slot1Button.removeNode()
        self.slot2Button.removeNode()
        self.slot3Button.removeNode()
        self.slot4Button.removeNode()
        if self.popupText: self.popupText.removeNode()