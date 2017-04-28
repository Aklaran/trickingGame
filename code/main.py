from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

from play import TrickingGame
from menu import MainMenu
from save import Save
from load import Load
from stats import Stats
from tricker import Tricker


# TODO: Make a screen/menu class that has functions like popuptext, transitions, etc
# NOTE: In order to run this properly, put these 2 lines in your config.prc file of your panda installation:
'''
clode-mode limited
clock-frame-rate 20
'''
# This will ensure all the shit moves in the right time :P

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.tricker = Tricker()

        self.gameFSM = GameFSM('Core Game FSM')
        self.gameFSM.demand('MainMenu')

class GameFSM(FSM):
    def enterMainMenu(self):
        self.menu = MainMenu()
    def exitMainMenu(self):
        self.menu.destroy()
        del self.menu
    def enterPlay(self):
        self.play = TrickingGame()
    def exitPlay(self):
        self.play.destroy()
        del self.play
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