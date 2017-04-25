from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

from play import TrickingGame
from menu import MainMenu
from save import Save
from load import Load
from tricker import Tricker

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

app = Main()
app.run()