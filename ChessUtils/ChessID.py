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

    # calibrateBoardPosition
    # Function to call at the beginning of programming execution
    # Displays video feed with dots for the four corners of the chessboard overlaid
    # Use to adjust camera and chessboard
    def calibrateBoardPosition(self):
        # Loop until 'q' key is pressed
        while(True):
            # Read in frame
            ret, frame = self.camera.read()

            # Draw circles on the four corners of the chessboard
            cv2.circle(frame, (self.squareCoords[0][2], self.squareCoords[0][1]), 5, (0,255,0), -1)
            cv2.circle(frame, (self.squareCoords[7][0], self.squareCoords[7][1]), 5, (0,255,0), -1)
            cv2.circle(frame, (self.squareCoords[56][2], self.squareCoords[56][3]), 5, (0,255,0), -1)
            cv2.circle(frame, (self.squareCoords[63][0], self.squareCoords[63][3]), 5, (0,255,0), -1)

            # Display image with circle
            cv2.imshow('Calibrate Board Position', frame)

            # Exit if q is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def getBoardState(self):
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

test.calibrateBoardPosition()
test.releaseCamera()

