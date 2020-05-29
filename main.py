from time import time

import mancala
import minimax


def play():
    board = mancala.Board()
    board.show()

    firstInput = input("Going first? (y/n): ").lower()
    if "y" in firstInput:
        playing = True
    else:
        playing = False

    while not board.noMoreMoves():
        if playing:

            print("\nSearching Minimax Tree w/ Alpha-Beta Pruning...")
            t = time()
            score, sequence = minimax.minimaxAlphaBeta(board)
            print(f"Finished calculations (time {(time() - t) * 1000:.2f}ms).")

            print(f"\nYour best move this turn: pot(s) {', then '.join([str(move + 1) for move in sequence[0]])}. ")

            for move in sequence[0]:
                playing, takeOpposite = board.playerMove(move)

        else:

            opponentMove = input("Enter the move your opponent made: ")
            notPlaying, takeOpposite = board.opponentMove(int(opponentMove) - 1)
            playing = not notPlaying
            if notPlaying:
                print("[GO AGAIN]")

        if takeOpposite:
            print("[TAKE OPPOSITE STONES]")

        board.show()




    if board.heuristicScore() > 0:
        print(f"I win ({board.state[6]} to {board.state[13]}! ")
    elif board.heuristicScore() < 0:
        print(f"Opponent wins ({board.state[13]} to {board.state[6]}! ")


# mancala.runAllTests()
print("Game self-tests successful.")

while True:
    play()

    again = input("Play again? (y/n): ").lower()
    if "n" in again:
        break

print("Program ended.")
