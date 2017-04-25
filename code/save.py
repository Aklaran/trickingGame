from direct.gui.DirectGui import *

import os
import json

class Save(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('Save')

        self.backButton = DirectButton(text=("back"), scale = 0.25,
                     command=self.switchToMainMenu, parent=base.a2dTopLeft,
                                       pos=(0.275,0,-0.225))
        self.slot1Button = DirectButton(text=('Empty Slot 1'),
                                        scale=0.1, pos=(0,0,.2),
                                        command=self.saveGame, extraArgs=['1'],
                                        parent=self.parentNode)
        self.slot2Button = DirectButton(text=('Empty Slot 2'),
                                        scale=0.1, pos=(0,0,0),
                                        command=self.saveGame, extraArgs=['2'],
                                        parent=self.parentNode)
        self.slot3Button = DirectButton(text=('Empty Slot 3'),
                                        scale=0.1,pos=(0,0,-.2),
                                        command=self.saveGame, extraArgs=['3'],
                                        parent=self.parentNode)
        self.slot4Button = DirectButton(text=('Empty Slot 4'),
                                        scale=0.1, pos=(0,0,-.4),
                                        command=self.saveGame, extraArgs=['4'],
                                        parent=self.parentNode)

    def saveGame(self, slot):
        saveFilePath = 'saves/save' + slot + '.json'
        projectPath = os.path.dirname(os.path.dirname((__file__)))
        fullFilePath = os.path.join(projectPath, saveFilePath)
        with open(fullFilePath, 'w+') as outfile:
            json.dump(base.tricker.saveDict, outfile,
                      sort_keys=True, indent=4, ensure_ascii=False)

    def switchToMainMenu(self):
        base.gameFSM.demand('MainMenu')

    def destroy(self):
        self.parentNode.removeNode()
        self.backButton.removeNode()
        self.slot1Button.removeNode()
        self.slot2Button.removeNode()
        self.slot3Button.removeNode()
        self.slot4Button.removeNode()
