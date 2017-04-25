from direct.gui.DirectGui import *

import os
import json

class Load(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('Load')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))
        self.slot1Button = DirectButton(text=('Empty Slot 1'),
                                        scale=0.1, pos=(0, 0, .2),
                                        command=self.loadGame, extraArgs=['1'],
                                        parent=self.parentNode)
        self.slot2Button = DirectButton(text=('Empty Slot 2'),
                                        scale=0.1, pos=(0, 0, 0),
                                        command=self.loadGame, extraArgs=['2'],
                                        parent=self.parentNode)
        self.slot3Button = DirectButton(text=('Empty Slot 3'),
                                        scale=0.1, pos=(0, 0, -.2),
                                        command=self.loadGame, extraArgs=['3'],
                                        parent=self.parentNode)
        self.slot4Button = DirectButton(text=('Empty Slot 4'),
                                        scale=0.1, pos=(0, 0, -.4),
                                        command=self.loadGame, extraArgs=['4'],
                                        parent=self.parentNode)


    def loadGame(self, slot):
        print("old:", base.tricker.saveDict)
        saveFilePath = 'saves/save' + slot + '.json'
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        with open(fullFilePath, 'r') as infile:
            base.tricker.saveDict = json.load(infile)
            base.tricker.totalStam = base.tricker.saveDict['totalStam']
            base.tricker.name = base.tricker.saveDict['name']
            base.tricker.level = base.tricker.saveDict['level']
            print(base.tricker.saveDict)

    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
