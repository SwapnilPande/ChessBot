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

        # Define standard message headers in arduino-laptop communication interfaces
        self.initHandshakeHeader = b"\x01"

        # Perform initialization handshake to ensure arduino is ready
        self.initHandshake()

    # Reads all messages in buffer to clear
    # Use only between commands when confident arduino is not sending data
    def clearBuffer(self):
        messagedReceived = b""

    # Perform initialization handshake signifying laptop is ready to begn
    # Waits until init handshake is received from Arduino before proceeding
    def initHandshake(self):
        received = b""
        # loop until a initialization message is received
        while(self.ser.read(1) != self.initHandshakeHeader):
            self.ser.write(self.initHandshakeHeader)


    # Function to wait for the player to make a move
    # Arduino sends command over serial when player makes a move (presses the button)
    def waitForPlayerMove(self):
        while True:
            self.ser.write(b'\x10')
            print(self.ser.read(1))
            #print(b'\x10'[0])
            time.sleep(2)
            # out = self.ser.read(1)
            # if(len(out) > 0):
            #     print(out[0])

    # Function to send the computer to move to the arduino
    def sendComputerMove(self):
        #TODO Write function
        return

test = ArduinoInterface()
test.initHandshake()
print("Successfully initialized")





