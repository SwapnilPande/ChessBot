import chess


class ChessGameDriver():

    def __init__(self):


        self.board = None

    def startNewGame(self):
        self.board = chess.Board()

    # addPlayerMove
    # Adds the players move to the computer's representation of the chess board
    # piecePositions - list of length 64 (number of squares) containing the piece in each square
    def addPlayerMove(self, piecePositions):
        #Calculate change in position from previous board to current board
        san =

        board.push_san(san)

        self.prevPiecePositions = piecePositions

    def getBoard():
        return self.board

