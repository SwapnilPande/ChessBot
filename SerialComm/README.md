# Arduino-Laptop Communication Protocol

## Message Header

Each message will be proceeded by a header byte specifying what data is being sent. The length of the message will be fixed for each message type.

* 0x01 - Initialization Handshake
* 0x02 - Move Chess Piece
* 0x04 - Button pressed, player has made move
* 0x08 - Command received confirmation
* 0x10 - Command completed confirmation
* 0x20 - Reset
* 0x40 - Shutdown


## **Handshake** - Header `0x01`
 The message has no payload (it only consists of the header). When the laptop has fully performed intialization steps, it repeatedly sends an initialization message to the Arduino. When the Arduino has performed it's initialization step, it waits to receive the initialization message from the laptop. On receipt, the Arduino will respond with an initialization method signifying that the initialization handshake is complete.

 ## **Move Chess Piece** - Header `0x02`
 This message is sent to command the Arduino to move the chess piece for the computer player. The message payload consists of three integers:

 * Original Position - Original position of the chess piece to be moved. This is a value in the range 0-63, with each value representing a unique square on the chess board.
 * New Position - New position for the chess piece. This is also a value in the range of 0-63, representing a unique square.
 * Capture - Either contains a 0 or 1. Signifies that the piece that is being moved is capturing the piece at the new position. This exists to allow the Arduino to execute custom logic to move the captured piece.

## **Button Pressed** - Header `0x04`
This message is sent from the Arduino to the laptop when the button has been pressed signifying that the player has made a move. This signals to the laptop to follow the process to capture image of chessboard and to make a computer move. The message has no payload. When the laptop receives the command, it will respond with a Command received confirmation byte.

## **Reset** - Header `0x20`
This message is sent from the laptop to the arduino when the human user gives a reset command to the application. The message has no payload. On receipt, the Arduino will send a command received message. After completing the reset procedure, the Arduino will send a command completed message and wait for a command received message.

## **Shutdown** - Header `0x40`
This message is sent from the laptop to the arduino when the human user gives a shutodwn command to the application. The message has no payload. On receipt, the Arduino will send a command received message. After completing the reset procedure, the Arduino will send a command completed message and wait for a command received message.


## **Command Received Confirmation** - Header `0x08`
This message is sent in response to any message sent from the laptop to Arduino or Arduino to laptop. This is the response to confirm that a message was received and the command is being executed. This message has no payload.

## **Command Complete Confirmation** - Header `0x10`
This message is sent from the Arduino to laptop when the Arduino is sent a command that will take a while to execute. This is the response to confirm that the command has been executed and the Arduino is ready to proceed to the next state of the game. This message has no payload.