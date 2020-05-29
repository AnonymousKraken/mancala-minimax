def minimaxAlphaBeta(board, depth=7, alpha=-999, beta=999, isAI=True, sequence=[]):
    if depth == 0 or board.noMoreMoves():
        return board.heuristicScore(), sequence
    if isAI:
        maxScore = -999
        bestSequence = []
        for newBoard, move in board.flat(board.possiblePlayerMoves()):
            score, seq = minimaxAlphaBeta(newBoard, depth - 1, alpha, beta, False, sequence + [move])
            if score > maxScore:
                maxScore = score
                bestSequence = seq
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore, bestSequence

    else:
        minScore = 999
        bestSequence = []
        for newBoard, move in board.flat(board.possibleOpponentMoves()):
            score, seq = minimaxAlphaBeta(newBoard, depth - 1, alpha, beta, True, sequence)
            if score < minScore:
                minScore = score
                bestSequence = seq
            beta = min(beta, score)
            if beta <= alpha:
                break
        return minScore, bestSequence
