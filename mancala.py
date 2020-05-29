class Board:

    def __init__(self, board=None):
        if board is None:
            self._state = [4, 4, 4, 4, 4, 4, 0] * 2
        else:
            self._state = board.state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        self._state = newState
        assert sum(self.state) == 48, f"\nExpected 48, got {sum(self.state)}. " \
                                      f"\nBoard:      {self.state}. " \
                                      f"\nOpp. board: {self.stateOpponent}."

    @property
    def statePlayer(self):
        return self.state[:-1]

    @statePlayer.setter
    def statePlayer(self, newState):
        self.state = newState + [self.state[-1]]

    @property
    def stateOpponent(self):
        return self.state[:6] + self.state[7:]

    @stateOpponent.setter
    def stateOpponent(self, newState):
        self.state = newState[:6] + [self.state[6]] + newState[6:]

    def playerMove(self, bowl):
        assert bowl < 6
        board = self.statePlayer
        newBoard, endBowl = self.move(board, bowl)
        self.statePlayer = newBoard

        # New turn rule
        if endBowl == 6:
            return True, False
        # Taking opposite on empty
        elif endBowl < 6 and newBoard[endBowl] == 1:
            self._state[6] += self.state[12 - endBowl] + 1
            self._state[12 - endBowl] = 0
            self._state[endBowl] = 0

            return False, True

        return False, False

    def opponentMove(self, bowl):
        assert bowl < 6
        bowl += 6
        state = self.stateOpponent
        newState, endBowl = self.move(state, bowl)
        self.stateOpponent = newState

        # New turn rule
        if endBowl == 12:
            return True, False
        # Taking opposite on empty
        elif 5 < endBowl < 12 and newState[endBowl] == 1:
            self._state[13] += self.state[11 - endBowl] + 1
            self._state[11 - endBowl] = 0
            self._state[endBowl+1] = 0

            return False, True

        return False, False

    def move(self, board, bowl):
        stones = board[bowl]
        assert stones > 0
        board[bowl] = 0

        for stone in range(stones):
            bowl = (bowl + 1) % len(board)
            board[bowl] += 1

        return board, bowl

    def possiblePlayerMoves(self, board=None, sequence=[]):
        if board is None:
            board = self
        for i in range(6):
            if board.state[i] != 0:
                newBoard = Board(board)
                continueTurn, takeOpposite = newBoard.playerMove(i)
                if continueTurn:
                    yield list(self.possiblePlayerMoves(newBoard, sequence + [i]))
                else:
                    yield newBoard, sequence + [i]

    def possibleOpponentMoves(self, board=None, sequence=[]):
        if board is None:
            board = self
        for i in range(6):
            if board.state[i + 7] != 0:
                newBoard = Board(board)
                continueTurn, takeOpposite = newBoard.opponentMove(i)
                if continueTurn:
                    yield list(self.possibleOpponentMoves(newBoard, sequence + [i]))
                else:
                    yield newBoard, sequence + [i]

    def flat(self, moves):
        flattenedMoves = []
        for move in moves:
            if type(move) == list:
                flattenedMoves += self.flat(move)
            else:
                flattenedMoves.append(move)
        return flattenedMoves

    def noMoreMoves(self):
        return not any(self.state[:6]) or not any(self.state[7:13])

    def heuristicScore(self):
        return self.state[6] - self.state[13]

    def show(self):
        print("\n@" + "-" * 23 + "@")
        print("|//|" + "|".join([str(i).ljust(2) for i in self.state[:6]]) + "|//|")
        print(f"|{self.state[6]:<2}|" + "." * 17 + f"|{self.state[13]:<2}|")
        print("|//|" + "|".join([str(i).ljust(2) for i in self.state[7:13]]) + "|//|")
        print("@" + "-" * 23 + "@\n")


def moveAround():
    board = Board()
    board.opponentMove(5)
    board.playerMove(1)
    assert board.state == [5, 0, 6, 5, 5, 5, 1, 4, 4, 4, 4, 4, 0, 1], f"Got {board.state}."


def mancalaSkip():
    board = Board()
    board.state = []


if __name__ == "__main__":
    board = Board()
    for move in board.flat(board.possiblePlayerMoves()):
        print(move)
    # board.playerMove(0)
    # moveAround()
