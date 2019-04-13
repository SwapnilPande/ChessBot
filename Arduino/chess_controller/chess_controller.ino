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
#define RPM 240
#define DIRECTION_PIN_X 8
#define STEP_PIN_X 9
#define DIRECTION_PIN_Y 6
#define STEP_PIN_Y 7
#define MICROSTEPS 1

#define DEGREES_PER_SQUARE 2162.162162
#define DEGREE_OFFSET_X 900 // Offset from the 0 position to the middle of the first square
#define DEGREE_OFFSET_Y 350
double currentSquareX;
double currentSquareY;

// MAGNET PIN
#define MAGNET_PIN 3

// Initialize Stepper Motor Drivers here
DRV8825 stepperX(STEPS_PER_REV, DIRECTION_PIN_X, STEP_PIN_X);
DRV8825 stepperY(STEPS_PER_REV, DIRECTION_PIN_Y, STEP_PIN_Y);


//////////////////// MAGNET CODE
void magnetInit()
{
  pinMode(MAGNET_PIN, OUTPUT);
}

void magnetOn()
{
  digitalWrite(MAGNET_PIN,HIGH);
  delay(250);
}

void magnetOff()
{
  digitalWrite(MAGNET_PIN,LOW);
  delay(250);
}



// These two functions calculate how much to move the motors to move to the desired square
void moveToXCoordinate(double squareCoord)
{
  stepperX.rotate(DEGREES_PER_SQUARE*(squareCoord - currentSquareX));
  currentSquareX = squareCoord;
}

void moveToYCoordinate(double squareCoord)
{
  stepperY.rotate(DEGREES_PER_SQUARE*(squareCoord - currentSquareY));
  currentSquareY = squareCoord;
}

void makeMove(double startX, double startY, double finalX, double finalY)
{
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
  moveToYCoordinate(finalY-.1);

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
  byte originalCoordinate = Serial.read();
  while(Serial.available() < 1)
  {}
  byte newCoordinate = Serial.read();
  while(Serial.available() < 1)
  {}
  byte capture = Serial.read();
  
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

//  //// TEST CODE
//  if(originalCoordinate == 10 && newCoordinate == 15 && capture == 0)
//  {
//    digitalWrite(13, HIGH);
//  }

  //TODO impelement chess piece moving code

  // Send command completed message
  while(Serial.read() != COMMAND_RECEIVED_HEADER)
  {
    Serial.write(COMMAND_COMPLETED_HEADER);
    delay(0.1);
  }
}

void reset()
{
  // Initial Stepper motor positions
  currentSquareX = 0;
  currentSquareY = 0;

  //TODO impelement reset procedure
  delay(5000);

  // Send command completed message
  while(Serial.read() != COMMAND_RECEIVED_HEADER)
  {
    Serial.write(COMMAND_COMPLETED_HEADER);
    delay(0.1);
  }
  digitalWrite(13, HIGH);
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
  digitalWrite(13, HIGH);
}

void waitForPlayerMove()
{
  delay(1000);
  //while(button is not pressezd)
//  {
//    // do nothing
//  }
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
  while(true)
  {
    if(Serial.available() > 0)
    {
      message = Serial.read();
      switch(message)
      {
        case MOVE_PIECE_HEADER:
          moveChessPiece();
          break;
        case RESET_HEADER:
          reset();
          break;
        case SHUTDOWN_HEADER:
          shutdownRobot();
          break;
      }
    }
  }
}


void setup() {
  Serial.begin(9600);

  magnetInit();

  // Init stepper motors
  stepperX.begin(RPM, MICROSTEPS);
  stepperY.begin(RPM, MICROSTEPS);

  // Move motors to (0x0) square
  stepperX.rotate(DEGREE_OFFSET_X);
  stepperY.rotate(DEGREE_OFFSET_Y);
  
  //initHandshake();
  //waitForNextCommand();
  Serial.println("testing");

  magnetOff();

}

int degree;
int curDegree;

int currCoord = 0;
int prevCoord = 0;
void loop() {
  
  if (Serial.available() > 0) {
    // read the incoming byte:
    currCoord = Serial.parseInt();

    while(Serial.available())
    {
      degree = Serial.read();
    }

    makeMove(2, 0, 2, 2);
    prevCoord = currCoord;
  }
  
}
