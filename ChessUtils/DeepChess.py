import ChessBot

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

    # Returns a list of legal moves for the BLACK PLAYER
    # board is a chess board object
    def getLegalMoves(self, board):
        return

    def generateMove(self, board):
        # Determine all legal moves

        # Perform alpha-beta search to find optimal move

        # Return better move



