from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

from play import TrickingGame
from menu import MainMenu
from save import Save

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

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

app = Main()
app.run()