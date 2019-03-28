#define INIT_HANDSHAKE_HEADER 0x01
#define MOVE_PIECE_HEADER 0x02
#define BUTTON_PRESSED_HEADER 0x04
#define COMMAND_RECEIVED_HEADER 0x08
#define COMMAND_COMPLETED_HEADER 0x10
#define RESET_HEADER 0x20
#define SHUTDOWN_HEADER 0x40

int incomingByte = 0;

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
  pinMode(13, OUTPUT);
  initHandshake();
  waitForNextCommand();

}

void loop() {
}
