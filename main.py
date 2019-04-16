from ChessUtils.ChessID import ChessID
from ChessUtils.ChessGameDriver import ChessGameDriver
from ChessUtils.DeepChess import DeepChess
import chess

from SerialUtils.ArduinoInterface import ArduinoInterface

# Initialize Chess ID module
chessid = ChessID()
# Calibrate the chess board position
chessid.calibrateBoardPosition()

deepchess = DeepChess()

# Initialize Chess Game Driver
chessDriver = ChessGameDriver()

# Start a new chess game
chessDriver.startNewGame()

# Create the Arduino Serial interface object
arduino = ArduinoInterface()
# Perform initialization handshake with Arduino
arduino.initHandshake()




print("INFO: Completed Initialization")

shutdown = False
while(not shutdown):
    print(chessDriver.board)

    arduino.waitForPlayerMove()

    piecePredictions = chessid.getBoardState()

    chessDriver.addPlayerMove(piecePredictions)

    print(chessDriver.board)

    startSquare, endSquare, capture = deepchess.generateMove(chessDriver.getBoard())
    print(startSquare)
    print(endSquare)
    print(capture)

    arduino.moveChessPiece(startSquare, endSquare, capture)









