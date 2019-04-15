import chess
import time

class ChessGameDriver():

    def __init__(self):


        self.board = None

        # Define square names for each square index
        self.rankNames = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.fileNames = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.squareNames = [f + r for r in self.rankNames for f in self.fileNames]

    def startNewGame(self):
        # Initialize a new empty chess board
        self.board = chess.Board()

        self.prevPiecePositions = [ None ] * 64

        # Initialize previous position to a new chess board
        self.prevPiecePositions[0] = "R"
        self.prevPiecePositions[1] = "N"
        self.prevPiecePositions[2] = "B"
        self.prevPiecePositions[3] = "Q"
        self.prevPiecePositions[4] = "K"
        self.prevPiecePositions[5] = "B"
        self.prevPiecePositions[6] = "N"
        self.prevPiecePositions[7] = "R"
        for i in range(8,16):
            self.prevPiecePositions[i] = "P"
        for i in range(16, 48):
            self.prevPiecePositions[i] = "empty"
        for i in range(48, 56):
            self.prevPiecePositions[i] = "p"
        self.prevPiecePositions[56] = "r"
        self.prevPiecePositions[57] = "n"
        self.prevPiecePositions[58] = "b"
        self.prevPiecePositions[59] = "q"
        self.prevPiecePositions[60] = "k"
        self.prevPiecePositions[61] = "b"
        self.prevPiecePositions[62] = "n"
        self.prevPiecePositions[63] = "r"


    # addPlayerMove
    # Adds the players move to the computer's representation of the chess board
    # piecePositions - list of length 64 (number of squares) containing the piece in each square
    def addPlayerMove(self, piecePositions):
        # differences stores the chess pieces that have changed between consecutive boards
        differences  = []
        # Iterate over all pairs of pieces
        for i, (previousPiece, curPiece) in enumerate(zip(self.prevPiecePositions, piecePositions)):
            if previousPiece != curPiece:
                differences.append(i)

        # Error: Detected too many or too few move changes - must enter move manually
        if(len(differences) != 2):
            startSquare, endSquare = self.manuallyAddPlayerMove()
        else:
            # Check which of the two squares went from empty to non-empty
            if(self.prevPiecePositions[differences[0]] != "empty" and piecePositions[differences[0]] == "empty"):
                startSquare = differences[0]
                endSquare = differences[1]
            elif(self.prevPiecePositions[differences[1]] != "empty" and piecePositions[differences[1]] == "empty"):
                startSquare = differences[1]
                endSquare = differences[0]

            # Neither square went from empty to non-empty, ask user to manually enter move
            else:
                startSquare, endSquare = self.manuallyAddPlayerMove()

        # Push move to board
        self.board.push(chess.Move(startSquare, endSquare))

        # Generated updated piece positions
        for i in range(64):
            piece = self.board.piece_at(i)
            if(piece == None):
                self.prevPiecePositions[i] = "empty"
            else:
                self.prevPiecePositions[i] = str(piece)

    def manuallyAddPlayerMove(self):
        print("ERROR: Unable to detect player move. Please enter move manually")
        startSquare = input("Start Square: ")
        endSquare = input("End Square: ")
        return int(startSquare), int(endSquare)


    def getBoard():
        return self.board

test = ChessGameDriver()
test.startNewGame()

testPos = [ None ] * 64
testPos[0] = "empty"
testPos[1] = "empty"
testPos[2] = "B"
testPos[3] = "Q"
testPos[4] = "K"
testPos[5] = "B"
testPos[6] = "N"
testPos[7] = "R"
for i in range(8,16):
    testPos[i] = "P"
for i in range(16, 48):
    testPos[i] = "empty"
for i in range(48, 56):
    testPos[i] = "p"
testPos[16] = "N"
testPos[56] = "r"
testPos[57] = "n"
testPos[58] = "b"
testPos[59] = "q"
testPos[60] = "k"
testPos[61] = "b"
testPos[62] = "n"
testPos[63] = "r"
test.addPlayerMove(testPos)
print(test.board)
test.addPlayerMove(testPos)

print(test.board)
