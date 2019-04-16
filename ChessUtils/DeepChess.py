import random

class DeepChess:
    def __init__(self):
        #Initialize neural network

        # Search depth for alpha-beta search
        self.searchDepth = None

    def getBitboard(self, board):
        """
            A bitboard is a representation of the current board state
            There are a total of 64 squares on the board, 6 pieces, and 2 colors
            Each unique piece/color has 64 indices, with a 1 indicating that the piece exists at that location
            4 extra indices are for castling rights on each size
            1 extra index indicates whose turn it is
        """
        bitboard = np.zeros(2*6*64  + 5)

        pieceIndices = {
            'p': 0,
            'n': 1,
            'b': 2,
            'r': 3,
            'q': 4,
            'k': 5}

        for i in range(64):
            if board.piece_at(i):
                color = int(board.piece_at(i).color)
                bitboard[(6*color + pieceIndices[board.piece_at(i).symbol().lower()] + 12*i)] = 1

        bitboard[-1] = int(board.turn)
        bitboard[-2] = int(board.has_kingside_castling_rights(True))
        bitboard[-3] = int(board.has_kingside_castling_rights(False))
        bitboard[-4] = int(board.has_queenside_castling_rights(True))
        bitboard[-5] = int(board.has_queenside_castling_rights(False))

        return bitboard

    # compareBoards
    # Takes in 2 boards and returns the better board position for the BLACK player
    # board1 and board2 are the two boards to compare
    def compareBoards(self, board1, board2):
        # Generate two bitboards
        bitboard1 = self.getBitboard(board1)
        bitboard2 = self.getBitboard(board2)

        # Feed bitboards into neural network

        # Return better bitboard


    def generateMove(self, board):
        alpha = -1
        beta = 1
        v = -1
        depth = 2
        moves = []
        bestMove = None
        for move in board.legal_moves:
            if((not board.is_kingside_castling(move)) and (not board.is_queenside_castling(move))):
                moves.append(move)
                if(board.is_capture(move)):
                    bestMove = move
        if(bestMove == None):
            bestMove = random.choice(moves)
        capture = board.is_capture(bestMove)
        board.push(bestMove)
        #     cur = copy.copy(board)
        #     cur.push(move)
        #     if v == -1:
        #         v = self.alphabeta(cur, depth-1, alpha, beta, False)
        #         bestMove = move
        #         if alpha == -1:
        #             alpha = v
        #     else:
        #         new_v = self.predict(self.alphabeta(cur, depth-1, alpha, beta, False), v)[0]
        #         if new_v != v:
        #             bestMove = move
        #             v = new_v
        #         alpha = self.predict(alpha, v)[0]

        # print(bestMove)
        # board.push(bestMove)
        return bestMove.from_square, bestMove.to_square, capture

        # Perform alpha-beta search to find optimal move

        # Return better move


    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return node
        if maximizingPlayer:
            v = -1
            for move in node.legal_moves:
                cur = copy.copy(node)
                cur.push(move)
                if v == -1:
                    v = alphabeta(cur, depth-1, alpha, beta, False)
                if alpha == -1:
                    alpha = v

                v = netPredict(v, alphabeta(cur, depth-1, alpha, beta, False))[0]
                alpha = netPredict(alpha, v)[0]
                if beta != 1:
                    if netPredict(alpha, beta)[0] == alpha:
                        break
            return v
        else:
            v = 1
            for move in node.legal_moves:
                cur = copy.copy(node)
                cur.push(move)
                if v == 1:
                    v = alphabeta(cur, depth-1, alpha, beta, True)
                if beta == 1:
                    beta = v

                v = netPredict(v, alphabeta(cur, depth-1, alpha, beta, True))[1]
                beta = netPredict(beta, v)[1]
                if alpha != -1:
                    if netPredict(alpha, beta)[0] == alpha:
                        break
            return v

    #def computerMove(board, depth):




