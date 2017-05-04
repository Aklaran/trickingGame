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
        self.slot1Button = None
        self.slot2Button = None
        self.slot3Button = None
        self.slot4Button = None
        self.backButton = None
        self.background = None

        self.guiElements = []

    def disableGUI(self):
        for element in self.guiElements:
            element['state'] = DGG.DISABLED
    def enableGUI(self):
        for element in self.guiElements:
            element["state"] = DGG.NORMAL

    def switchToMainMenu(self):
        base.gameFSM.demand('StartMenu')

    def switchToSave(self):
        base.gameFSM.demand('Save')

    def switchToLoad(self):
        base.gameFSM.demand('Load')

    def switchToControls(self):
        base.gameFSM.demand('Controls')

    def switchToStats(self):
        if base.player1.hasName() or base.player2.hasName():
            base.gameFSM.demand('Stats')
        else:
            s = 'No character selected.'
            self.drawPopupText(s)

    def clearText(self):
        self.nameEntry.enterText('')

    @staticmethod
    def getSaveFilePath(slot):
        if os.name == 'nt':
            return 'saves\save' + slot + '.json'
        else:
            return 'saves/save' + slot + '.json'

    def loadButtonData(self, slot):
        #pulls data for each slot from the corresponding .json file
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

    # this just draws the text - DO NOT CALL. instead, call drawPopupText()
    def createPopupText(self,s):
        self.popupText = OnscreenText(text=s, scale = 0.1, parent=base.a2dTopCenter,
                                      pos = (0,-.75) )

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
        if self.backButton: self.backButton.removeNode()
        if self.slot1Button: self.slot1Button.removeNode()
        if self.slot2Button: self.slot2Button.removeNode()
        if self.slot3Button: self.slot3Button.removeNode()
        if self.slot4Button: self.slot4Button.removeNode()
        if self.nameEntry: self.nameEntry.removeNode()
        if self.background: self.background.removeNode()