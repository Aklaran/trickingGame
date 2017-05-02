import os
import json
from pathlib import Path
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.gui.DirectGui import *

class Menu(object):
    def __init__(self):
        self.parentNode = None
        self.popupText = None
        self.popupSeq = None
        self.nameEntry = None

    def switchToMainMenu(self):
        base.gameFSM.demand('StartMenu')

    def switchToSave(self):
        base.gameFSM.demand('Save')

    def switchToLoad(self):
        base.gameFSM.demand('Load')

    def switchToStats(self):
        if base.currPlayer.hasName():
            base.gameFSM.demand('Stats')
        else:
            s = 'No save data found. Press Play to make a character!'
            self.drawPopupText(s)

    def clearText(self):
        self.nameEntry.enterText('')

    def switchToTrain(self):
        if base.currPlayer.hasName():
            base.gameFSM.demand('Train')
        else:
            self.nameEntry = DirectEntry(text="", scale=0.1, command=self.callSetNameAndDemandTrain,
                                             initialText="Enter Name", focus=1, focusInCommand=self.clearText,
                                             frameSize=(0, 15, 0, 1))

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
        else:
            return None

    def createPopupText(self,s):
        self.popupText = OnscreenText(text=s, scale = 0.07, parent=base.a2dTopCenter,
                                      pos = (0,-.05) )

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
        if self.nameEntry: self.nameEntry.removeNode()