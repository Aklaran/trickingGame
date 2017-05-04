from direct.task import Task
from direct.gui.DirectGui import *

from battleData import BattleData
from play import Play

import random


class BattleMode(Play):
    def __init__(self):
        super().__init__()

        self.battleData = BattleData()

        self.oppScoreText  = OnscreenText(pos=(0.5, -0.4), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.p1RoundText = OnscreenText(pos=(0.3, 0.2), scale = 0.1,
                                        parent = base.a2dBottomLeft, fg=(1,1,1,1))
        self.p2RoundText = OnscreenText(pos=(-0.3, 0.2), scale=0.1,
                                        parent=base.a2dBottomRight, fg=(1, 1, 1, 1))

        self.endGameDialog = None

        taskMgr.add(self.drawUITask, 'drawUI', extraArgs=['battle'],
                    appendTask=True)

        taskMgr.add(self.checkGameStateTask, 'checkGameState')

        self.showInitialDialog()

    def showInitialDialog(self):
        self.ignoreAll()
        initialStr = "- BATTLE MODE - \n" \
                     "Chain together tricks to make dope combos and outscore your opponent. \n" \
                     "Hit the button too early or run out of stamina, and you'll fall, halving your score. \n" \
                     "First to three rounds wins!"
        self.initialDialog = DirectDialog(dialogName="initialDialog", scale=1,
                                          text=initialStr,
                                          buttonTextList=['Roll for turn'],
                                          command=self.rollForTurn)
    def rollForTurn(self, arg):
        player = random.randint(1,2)
        if player == 1:
            base.currPlayer = base.player1
        elif player == 2:
            base.currPlayer = base.player2
        base.firstBattle = False
        if self.initialDialog: self.initialDialog.detachNode()
        s = base.currPlayer.getName() + " won the roll. Throw your first pass!"
        self.drawPopupText(s)
        self.reset()

    def checkGameStateTask(self, task):
        if base.currPlayer.comboHasEnded():
            self.ignoreAll()
            taskMgr.doMethodLater(2, self.changeTurnTask, 'changeTurn',
                                  extraArgs=[base.currPlayer, False], appendTask=True)
            return Task.done
        elif base.currPlayer.isFalling():
            self.ignoreAll()
            taskMgr.doMethodLater(4, self.changeTurnTask, 'changeTurn',
                                  extraArgs=[base.currPlayer, True], appendTask=True)
            return Task.done
        return Task.cont

    def changeTurnTask(self, currPlayer, falling, task):
        self.battleData.updateScore(currPlayer, int(currPlayer.getScore()), falling)
        currPlayer.reset()
        s = self.battleData.checkEndRound()
        if s: self.drawPopupText(s)
        winner = self.battleData.checkEndGame()
        if winner:
            taskMgr.doMethodLater(1, self.showEndGameDialogTask, 'EndGameDialog', extraArgs=[winner], appendTask=True)
            return Task.done
        if currPlayer == base.player1:
            base.setPlayer(base.player2)
        elif currPlayer == base.player2:
            base.setPlayer(base.player1)
        self.reset()
        return Task.done

    def showEndGameDialogTask(self, winner, taskMgr):
        endGameStr = winner.getName() + " wins!"
        self.endGameDialog = DirectDialog(dialogName="endGameDialog", scale=1,
                                       text=endGameStr,
                                       buttonTextList=['Quit', 'Rematch'],
                                       buttonValueList=['quit', 'rematch'],
                                       command=self.endGameItemSel)
    def endGameItemSel(self, arg):
        if arg == 'quit':
            self.switchToMainMenu()
        elif arg == 'rematch':
            self.battleData.__init__()
            base.currPlayer = base.player1
            self.rollForTurn(arg) #this arg is useless.. but necessary becuase i didnt want to write another

    def reset(self):
        # taskMgr.remove("follow")
        # base.currPlayer.actor.setPos(0, 0, 0)
        # self.trickerDummyNode.setPos(base.currPlayer.actor, (0,0,3))
        # self.nameText.setText(base.currPlayer.getName())
        self.ignoreAll()
        base.currPlayer.actor.detachNode()
        base.currPlayer.actor.reparentTo(self.parentNode)
        base.currPlayer.reset()
        self.destroy()
        self.reInit()


    def reInit(self):
        super().__init__()

        self.oppScoreText  = OnscreenText(pos=(0.5, -0.4), scale=0.1,
                                      parent=base.a2dTopLeft, fg=(1, 1, 1, 1))
        self.p1RoundText = OnscreenText(pos=(0.3, 0.2), scale = 0.1,
                                        parent = base.a2dBottomLeft, fg=(1,1,1,1))
        self.p2RoundText = OnscreenText(pos=(-0.3, 0.2), scale=0.1,
                                        parent=base.a2dBottomRight, fg=(1, 1, 1, 1))

        taskMgr.add(self.drawUITask, 'drawUI', extraArgs=['battle'],
                    appendTask=True)

        taskMgr.add(self.checkGameStateTask, 'checkGameState')

    def destroy(self):
        super().destroy()
        taskMgr.remove('changeTurn')
        self.oppScoreText.removeNode()
        self.p1RoundText.removeNode()
        self.p2RoundText.removeNode()
        if self.endGameDialog: self.endGameDialog.detachNode()