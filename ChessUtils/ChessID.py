import cv2
import numpy as np
from keras.models import load_model

class ChessID:
    def __init__(self):
        print("CHESSID: Beginning initialization")
        # Initiliaze camera
        self.camera = cv2.VideoCapture(1)

        # Path to file containing coordinates for chessboard squares
        self.coordinatePath = "ChessUtils/square_locations.txt"

        # Path to chess-id neural network model
        self.modelPath = "ChessUtils/final_chess-id_model.hdf5"
        self.model = load_model(self.modelPath)

        # List that stores the pixel coords of the squares on the chessboard
        self.squareCoords = []

        # Dimension of each individual square image
        self.squareImageDim = 227

        # Categories
        self.categories = ['b', 'k', 'n', 'p', 'q', 'r', 'empty', 'B', 'K', 'N', 'P', 'Q', 'R']

        with open(self.coordinatePath) as coordFile:
            for line in coordFile:
                line = line.replace("\n", "")
                self.squareCoords.append([int(x) for x in line.split(",")])

        self.calibrateBoardPosition()
        print("CHESSID: Initialization Success")
        print("")

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
        cv2.destroyAllWindows()


    def predict(self, squareImages):
        return self.model.predict(squareImages)

    def getBoardState(self):
        ret, frame = self.camera.read()

        frame = frame/255.0

        # Init empty np array to store the segmented square images
        squares = np.empty((64, self.squareImageDim, self.squareImageDim, 3))

        # Split each individual square image
        for i, squareCoord in enumerate(self.squareCoords):
            squares[i] = cv2.resize(frame[squareCoord[1]:squareCoord[3],
                                            squareCoord[0]:squareCoord[2],:],
                                (self.squareImageDim, self.squareImageDim))

        print("CHESS ID: Predicting Chess Piece Position")
        predictions = []
        for square in squares:
            out = self.predict(np.expand_dims(square, axis=0))[0]
            index = np.where(out == np.max(out))[0][0]

            predictions.append(self.categories[index])

        # Return piece at each square
        return predictions

    # Close camera device
    def releaseCamera(self):
        self.camera.release()

if __name__ == "__main__":
    test = ChessID()

    test.calibrateBoardPosition()
    board = test.getBoardState()

    for part in board:
        print(part)
    test.releaseCamera()

