from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM

#from main import TrickingGame

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.gameFSM = GameFSM('Core Game FSM')
        self.gameFSM.demand('MainMenu')



class MainMenu(object):
    def __init__(self):
        self.parentNode = aspect2d.attachNewNode('MainMenu')

        self.d = DirectButton(text=("Play"), scale = 0.25,
                     command=self.switchToPlay)
        #DirectButton(text=("Save/Load"))
        #DirectButton(text=("My Tricker"))
       # DirectButton(text=("Options"))

    def switchToPlay(self):
        print('sw')
        base.gameFSM.demand('Play')

    def destroy(self):
        self.parentNode.removeNode()
        self.d.destroy()

class GameFSM(FSM):
    def enterMainMenu(self):
        self.menu = MainMenu()

    def exitMainMenu(self):
        self.menu.destroy()

    def enterPlay(self):
        print('entering play')
    def exitPlay(self):
        print('exiting play')

app = Main()
app.run()