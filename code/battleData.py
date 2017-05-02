class BattleData(object):
    def __init__(self):
        self.p1Score = 0
        self.p2Score = 0
        self.p1Rounds = 0
        self.p2Rounds = 0
        self.roundsToWin = 1

    def getScore(self, player):
        if player == 1:
            return self.p1Score
        elif player == 2:
            return self.p2Score

    def getRounds(self, player):
        if player == 1:
            return self.p1Rounds
        elif player == 2:
            return self.p2Rounds

    def getOppScore(self):
        if base.currPlayer == base.player1:
            score = self.p2Score
        elif base.currPlayer == base.player2:
            score = self.p1Score
        return score
    def updateScore(self, tricker, score, falling):
        if falling:
            score == 1
        if tricker == base.player1:
            self.p1Score = score
            print("updated p1score:", self.p1Score)
        elif tricker == base.player2:
            self.p2Score = score
            print("updated p2score:", self.p2Score)

    def checkEndRound(self):
        if self.p1Score != 0 and self.p2Score != 0:
            if self.p1Score > self.p2Score:
                self.p1Rounds += 1
            elif self.p2Score > self.p1Score:
                self.p2Rounds += 1
            self.p1Score = self.p2Score = 0

    def checkEndGame(self):
        if self.p1Rounds == self.roundsToWin:
            return base.player1
        elif self.p2Rounds == self.roundsToWin:
            return base.player2
        return None

