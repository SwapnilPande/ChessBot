from ChessUtils.ChessID import ChessID
from ChessUtils.ChessGameDriver import ChessGameDriver
from ChessUtils.DeepChess import DeepChess
import chess

from SerialUtils import ArduinoInterface


# Create the Arduino Serial interface object
arduino = ArduinoInterface()
# Perform initialization handshake with Arduino
arduino.initHandshake()


# Initialize Chess ID module
chessid = ChessID()
# Calibrate the chess board position
chessid.calibrateBoardPosition()

deepchess = DeepChess()

# Initialize Chess Game Driver
chessDriver = ChessGameDriver()

# Start a new chess game
chessDriver.startNewGame()

shutdown = False
while(not shutdown):
    arduino.waitForPlayerMove()

    piecePredictions = chessid.predict()

    chessDriver.addPlayerMove(piecePredictions)

    startSquare, endSquare = deepchess.generateMove(chessDriver.getBoard())

    # TODO Convert move to chess board coordinate frame, check if move is capture
    # TODO FINISH IMPLEMENTING THIS FUNCTION
    # TODO ADD CODE TO IGNORE CASTLES
    arduino.moveChessPiece()









