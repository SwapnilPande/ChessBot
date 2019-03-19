# pySerial library
import Serial


class ArduinoInterface():
    """
        Arduino interface handles all serial communication to the arduino
        It provides simple API for waiting for input, sending commands, receiving commands, etc.
    """
    def __init__(self, baudRate = 9600, port = "COM7"):
        # Create a serial object
        self.ser = serial.Serial()
        self.ser.baudrate = baudRate
        self.ser.port = port
        self.ser.timeout = 1
        self.ser.open()

        # Perform initialization handshake to ensure arduino is ready
        self.initHandshake()

    def initHandshake(self):
        #TODO Define handshake procedure
        return

    # Function to wait for the player to make a move
    # Arduino sends command over serial when player makes a move (presses the button)
    def waitForPlayerMove(self):
        #TODO Write function
        return

    # Function to send the computer to move to the arduino
    def sendComputerMove(self):
        #TODO Write function
        return



