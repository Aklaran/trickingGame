from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

from play import TrickingGame
from menu import MainMenu

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

    def enterPlay(self):
        self.play = TrickingGame()
        print('entering play')
    def exitPlay(self):
        print('exiting play')

app = Main()
app.run()