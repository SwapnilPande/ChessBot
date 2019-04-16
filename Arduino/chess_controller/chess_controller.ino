// SERIAL MESSAGE HEADER DEFINITIONS
#define INIT_HANDSHAKE_HEADER 0x01
#define MOVE_PIECE_HEADER 0x02
#define BUTTON_PRESSED_HEADER 0x04
#define COMMAND_RECEIVED_HEADER 0x08
#define COMMAND_COMPLETED_HEADER 0x10
#define RESET_HEADER 0x20
#define SHUTDOWN_HEADER 0x40



#include "DRV8825.h"


// STEPPER MOTOR DRIVER DEFINITIONS
#define STEPS_PER_REV 200
#define RPM 360
#define DIRECTION_PIN_X 8
#define STEP_PIN_X 9
#define DIRECTION_PIN_Y 6
#define STEP_PIN_Y 7
#define MICROSTEPS 1

#define DEGREES_PER_SQUARE 2162.162162
#define DEGREE_OFFSET_X 660 // Offset from the 0 position to the middle of the first square
#define DEGREE_OFFSET_Y 300
#define MAX_X 19250
#define MAX_Y 17500

// Variables to store the current position of the motor
double currentSquareX;
double currentSquareY;
double currentDegreeX;
double currentDegreeY;

// MAGNET PIN
#define MAGNET_PIN 3
// BUTTON PIN
#define BUTTON_PIN 2

// Initialize Stepper Motor Drivers here
DRV8825 stepperX(STEPS_PER_REV, DIRECTION_PIN_X, STEP_PIN_X);
DRV8825 stepperY(STEPS_PER_REV, DIRECTION_PIN_Y, STEP_PIN_Y);


/////////////////// BUTTON CODE
void buttonInit()
{
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

//////////////////// MAGNET CODE
void magnetInit()
{
  pinMode(MAGNET_PIN, OUTPUT);
}

void magnetOn()
{
  analogWrite(MAGNET_PIN,200);
  delay(250);
}

void magnetOff()
{
  digitalWrite(MAGNET_PIN,LOW);
  delay(250);
}
//////////////////// END MAGNET CODE


//////////////////// MOTOR CONTROL CODE

void moveToXDegree(double degree)
{
  stepperX.rotate(degree - currentDegreeX);
  currentDegreeX = degree;
}

void moveToYDegree(double degree)
{
  stepperY.rotate(degree - currentDegreeY);
  currentDegreeY = degree;
}

// These two functions calculate how much to move the motors to move to the desired square
void moveToXCoordinate(double squareCoord)
{
  moveToXDegree(DEGREES_PER_SQUARE*squareCoord + DEGREE_OFFSET_X);
  currentSquareX = squareCoord;
}

void moveToYCoordinate(double squareCoord)
{
  moveToYDegree(DEGREES_PER_SQUARE*squareCoord + DEGREE_OFFSET_Y);
  currentSquareY = squareCoord;
}

void moveToMaxX()
{
  moveToXDegree(MAX_X);
}

void moveToMaxY()
{
  moveToYDegree(MAX_Y);
}

void returnToZero()
{
  moveToXDegree(0);
  moveToYDegree(0);
}

void makeMove(double startX, double startY, double finalX, double finalY, bool capture)
{
  // If this move is a capture
  if(capture)
  {
    // Move to capture piece position
    moveToXCoordinate(finalX);
    moveToYCoordinate(finalY);

    magnetOn();

    // Move to corner of square
    moveToXCoordinate(finalX+0.5);
    moveToYCoordinate(finalY+0.5);

    // Move to center of board
    moveToYCoordinate(4.5);
    // Release piece at edge of board
    moveToMaxX();

    magnetOff();
  }

  
  // Go to first square location
  moveToXCoordinate(startX);
  moveToYCoordinate(startY);

  magnetOn();

  // Move to corner of sqaure
  moveToXCoordinate(startX+0.5);
  moveToYCoordinate(startY+0.5);

  // Move to new square
  moveToXCoordinate(finalX+0.5);
  moveToYCoordinate(finalY+0.5);

  // Move to center of square
  moveToXCoordinate(finalX);
  moveToYCoordinate(finalY-0.1);

  magnetOff();

  moveToXCoordinate(finalX);
  moveToYCoordinate(finalY);
}




// Clears the serial buffer to prepare for the next instruction from the laptop
// Use only when confident laptop is not sending data
void clearSerialBuffer()
{
  while(Serial.available() > 0)
  {
    Serial.read();
  }
}

//Perform initialization handshake signifying Arduino is ready to begn
// Waits until init handshake is received from laptop before proceeding
void initHandshake()
{
  // Read in received data
  int receivedData = 0;

  // Loop waiting for laptop to send initialization handshake message
  while(receivedData != INIT_HANDSHAKE_HEADER)
  {
    receivedData = Serial.read();
  }
  Serial.write(INIT_HANDSHAKE_HEADER);
  Serial.write(INIT_HANDSHAKE_HEADER);

  // Clear serial buffer of all init messages and delay 1 second
  clearSerialBuffer();
  delay(1000);
}

// Sends a command received message to the laptop
// Clears the serial buffer after sending message
void messageSucessfulyReceived()
{
  Serial.write(COMMAND_RECEIVED_HEADER);
  clearSerialBuffer();
}

void moveChessPiece()
{
  // Read in payload of message
  while(Serial.available() < 1)
  {}
  int originalCoordinate = Serial.read();
  while(Serial.available() < 1)
  {}
  int newCoordinate = Serial.read();
  while(Serial.available() < 1)
  {}
  int capture = Serial.read();
  
  // Checking for errors in data
  if(originalCoordinate < 0 || originalCoordinate > 63)
  {
    return;
  }

  if(newCoordinate < 0 || newCoordinate > 63)
  {
    return;
  }

  if(capture != 0 && capture != 1)
  {
    return;
  }
  
  // If no errors in message, send messageSucessfulyReceived message
  messageSucessfulyReceived();

  // Convert coord in range 0-63 to (x,y) coord
  bool captureBool = (capture == 1);
  double startX = originalCoordinate%8;
  int intermediate = originalCoordinate/8;
  int startY = intermediate%8;

  double finalX = newCoordinate%8;
  intermediate = newCoordinate/8;
  int finalY = intermediate%8;
  makeMove(startX, startY, finalX, finalY, captureBool);

  // Send command completed message
  while(Serial.read() != COMMAND_RECEIVED_HEADER)
  {
    Serial.write(COMMAND_COMPLETED_HEADER);
    delay(0.1);
  }
}

void reset()
{
  // Turn off magnet and return to 0 square
  magnetOff();
  moveToXCoordinate(0);
  moveToYCoordinate(0);
 
  // Send command completed message
  while(Serial.read() != COMMAND_RECEIVED_HEADER)
  {
    Serial.write(COMMAND_COMPLETED_HEADER);
    delay(0.1);
  }
}

void shutdownRobot()
{
  // Send message successfully received message
  messageSucessfulyReceived();


  //TODO impelement reset procedure
  delay(5000);

  // Send command completed message
  while(Serial.read() != COMMAND_RECEIVED_HEADER)
  {
    Serial.write(COMMAND_COMPLETED_HEADER);
    delay(0.1);
  }
}

void waitForPlayerMove()
{
  
  while(digitalRead(BUTTON_PIN) != 0)
  { 
    // do nothing
  }
  while(Serial.read() != COMMAND_RECEIVED_HEADER)
  {
    Serial.write(BUTTON_PRESSED_HEADER);
    delay(0.1);
  }
  clearSerialBuffer();
  delay(1000);
}

// Waits for next command for laptop
// Depending on the message header received, function will call various other functions to perform actions
void waitForNextCommand()
{
  int message;
  bool commandExecuted = false;
  while(!commandExecuted)
  {
    if(Serial.available() > 0)
    {
      message = Serial.read();
        switch(message)
        {
          case MOVE_PIECE_HEADER:
            moveChessPiece();
            clearSerialBuffer();
            commandExecuted = true;
            break;
          case RESET_HEADER:
            reset();  
            commandExecuted = true;
            break;
          case SHUTDOWN_HEADER:
            shutdownRobot();
            commandExecuted = true;
            break;
        }
      }
  }
}


void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);

  magnetInit();
  buttonInit();
  // Init stepper motors
  stepperX.begin(RPM, MICROSTEPS);
  stepperY.begin(RPM, MICROSTEPS);

  

  magnetOff();
  
  initHandshake();

  // Move motors to (0x0) square
  moveToXDegree(DEGREE_OFFSET_X);
  moveToYDegree(DEGREE_OFFSET_Y); 

}

void loop() {
  waitForPlayerMove();
  waitForNextCommand();  
}
