from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

from train import TrainingMode
from battle import BattleMode
from startMenu import StartMenu
from save import Save
from load import Load
from stats import Stats
from tricker import Tricker

# TODO: All this shit
"""
dem animations
    really good raiz: guthrie slow 2:27
Modifynstats screen to work with 2 players

Make buttons not accept input when you're in a dialog/text entry
"""

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.player1 = Tricker()
        self.player2 = Tricker()
        self.currPlayer = self.player1

        self.gameFSM = GameFSM('Core Game FSM')
        self.gameFSM.demand('StartMenu')

    def setPlayer(self, player):
        self.currPlayer = player


class GameFSM(FSM):
    def enterStartMenu(self):
        self.menu = StartMenu()

    def exitStartMenu(self):
        self.menu.destroy()
        del self.menu

    def enterTrain(self):
        self.train = TrainingMode()

    def exitTrain(self):
        self.train.destroy()
        del self.train

    def enterBattle(self):
        self.battle = BattleMode()

    def exitBattle(self):
        self.battle.destroy()
        del self.battle

    def enterSave(self):
        self.save = Save()

    def exitSave(self):
        self.save.destroy()
        del self.save

    def enterLoad(self):
        self.load = Load()

    def exitLoad(self):
        self.load.destroy()
        del self.load

    def enterStats(self):
        self.stats = Stats()

    def exitStats(self):
        self.stats.destroy()
        del self.stats


app = Main()
app.run()
