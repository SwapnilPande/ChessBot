import cv2

class ChessID:
    def __init__(self):
        # Initiliaze camera
        self.camera = cv2.VideoCapture(1)

        # Path to file containing coordinates for chessboard squares
        self.coordinatePath = "square_locations.txt"

        self.squareCoords = []

        with open(self.coordinatePath) as coordFile:
            for line in coordFile:
                line = line.replace("\n", "")
                self.squareCoords.append([int(x) for x in line.split(",")])

        # Initialize neural network

    #def segmentChessBoard(self, image):


    def getBoardState(self):
        # Capture image
        ret, frame = self.camera.read()

        # squares each individual image of a square
        squares = []
        for squareCoord in self.squareCoords:
            squares.append(frame[squareCoord[0]:squareCoord[2],
                                squareCoord[1]:squareCoord[3],:])

        # Segment squares

        # Feed each square through neural network

        # Return piece at each square

    # Close camera device
    def releaseCamera(self):
        self.camera.release()


test = ChessID()

test.getBoardState()

