from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

from train import TrainingMode
from battle import BattleMode
from startMenu import StartMenu
from save import Save
from load import Load
from stats import Stats
from controls import Controls
from tricker import Tricker

# TODO: All this shit
"""
dem animations
    really good raiz: guthrie slow 2:27
    540
    initital for swing
    final for swing
    reversal falling
    bad anims:
        gswitch
        cork
        dbl cork
        btwist
        540
        raiz
        
slow mo

make citations:
    keyboard images:
        https://www.wpclipart.com/computer/keyboard_keys/

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

    def enterControls(self):
        self.controls = Controls()
    def exitControls(self):
        self.controls.destroy()
        del self.controls

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
