# pySerial library
import serial
import time


class ArduinoInterface():
    """
        Arduino interface handles all serial communication to the arduino
        It provides simple API for waiting for input, sending commands, receiving commands, etc.
    """
    def __init__(self, baudRate = 9600, port = "COM9"):
        # Create a serial object
        self.ser = serial.Serial()
        self.ser.baudrate = baudRate
        self.ser.port = port
        self.ser.timeout = 0.1
        self.ser.open()
        time.sleep(5)

        # Define standard message headers in arduino-laptop communication interfaces
        self.initHandshakeHeader = 1
        self.moveChessPieceHeader = 2
        self.buttonPressedHeader = 4
        self.commandReceivedHeader = 8
        self.commandCompletedHeader = 16
        self.resetHeader = 32
        self.shutdownHeader = 64

        # Perform initialization handshake to ensure arduino is ready
        self.initHandshake()

    # Reads all messages in buffer to clear
    # Use only between commands when confident arduino is not sending data
    def clearBuffer(self):
        while(self.ser.read(1) != b""):
            pass


    # Perform initialization handshake signifying laptop is ready to begn
    # Waits until init handshake is received from Arduino before proceeding
    def initHandshake(self):
        received = b""
        # loop until a initialization message is received
        while(self.ser.read(1) != bytes([self.initHandshakeHeader])):
            self.ser.write(bytes([self.initHandshakeHeader]))

        print("STATUS UPDATE: Initialization Procedure Complete")

        # Clear serial buffer of init messages and delay 1 secondt
        #self.clearBuffer()
        #time.sleep(1)
        return

    # Sends command to arduino to move chess piece from curPos to newPos
    #   curPos - current location of chess piece to move
    #   nextPos - position to move the chess piece to
    #   capture - boolean stating whether or not the move is capturing a piece
    def moveChessPiece(self, curPos, newPos, capture):
        print("STATUS UPDATE: Sending computer move")
        message = self.moveChessPieceHeader.to_bytes(1 , "little")
        message += curPos.to_bytes(1, "little")
        message += newPos.to_bytes(1, "little")
        message +=  (1 if capture else 0).to_bytes(1, "little")

        # Publish message until confirmation received that arduino received message
        while(self.ser.read(1) != self.commandReceivedHeader.to_bytes(1, "little")):
            self.ser.write(message)
            time.sleep(0.1)

        print("STATUS UPDATE: Waiting for robot to finish moving pieces")
        # Clear serial buffer of init messages and delay 1/2 second
        #self.clearBuffer()
        time.sleep(0.5)

        # Wait until Arduino sends a command completed message
        while(self.ser.read(1) != self.commandCompletedHeader.to_bytes(1, "little")):
            pass
        # Send confirmation that message was successfully received
        self.ser.write(self.commandReceivedHeader.to_bytes(1, "little"))
        print("STATUS UPDATE: Completed move")

        # Clear serial buffer of init messages and delay 1 second
        self.clearBuffer()
        time.sleep(1)

    # Function to wait for the player to make a move
    # Arduino sends command over serial when player makes a move (presses the button)
    def waitForPlayerMove(self):
        print("STATUS UPDATE: Waiting for player to make move...")
        while(self.ser.read(1) != bytes([self.buttonPressedHeader])):
            pass
        self.ser.write(self.commandReceivedHeader.to_bytes(1, "little"))
        self.clearBuffer()
        time.sleep(1)

    # Function to command the Arduino to perform shutdown routine
    def reset(self):
        print("STATUS UPDATE: Sending reset command to robot")
        message = self.resetHeader.to_bytes(1 , "little")
        while(self.ser.read(1) != self.commandReceivedHeader.to_bytes(1, "little")):
            self.ser.write(message)
            time.sleep(0.1)

        print("STATUS UPDATE: Waiting for robot to finish reset procedure")
        # Clear serial buffer and delay 1/2 second
        self.clearBuffer()
        time.sleep(0.5)

        # Wait until Arduino sends a command completed message
        while(self.ser.read(1) != self.commandCompletedHeader.to_bytes(1, "little")):
            pass
        # Send confirmation that message was successfully received
        self.ser.write(self.commandReceivedHeader.to_bytes(1, "little"))
        print("STATUS UPDATE: Completed reset procedure")

        # Clear serial buffer of init messages and delay 1 second
        self.clearBuffer()
        time.sleep(1)

    # Function to command the Arduino to perform shutdown routine
    def shutdown(self):
        print("STATUS UPDATE: Sending shutdown command to robot")
        message = self.shutdownHeader.to_bytes(1 , "little")
        while(self.ser.read(1) != self.commandReceivedHeader.to_bytes(1, "little")):
            self.ser.write(message)
            time.sleep(0.1)

        print("STATUS UPDATE: Waiting for robot to finish shutdown procedure")
        # Clear serial buffer of init messages and delay 1/2 second
        self.clearBuffer()
        time.sleep(0.5)

        # Wait until Arduino sends a command completed message
        while(self.ser.read(1) != self.commandCompletedHeader.to_bytes(1, "little")):
            pass
        # Send confirmation that message was successfully received
        self.ser.write(self.commandReceivedHeader.to_bytes(1, "little"))
        print("STATUS UPDATE: Shutdown complete")

        # Clear serial buffer of init messages and delay 1 second
        self.clearBuffer()
        time.sleep(1)

test = ArduinoInterface()
test.initHandshake()
print("Successfully initialized")
while(True):
    start = input("Start Position: ")
    finish = input("Finish Position: ")
    capture = input("Capture: ")

    test.moveChessPiece(int(start), int(finish), capture == "True")






