# Arduino-Laptop Communication Protocol

## Message Header

Each message will be proceeded by a header byte specifying what data is being sent. The length of the message will be fixed for each message type.

* 0x01 - Initialization Handshake
* 0x02 - Move Chess Piece
* 0x04 - Button pressed, player has made move
* 0x08 - Command received confirmation
* 0x10 - Reset
* 0x20 - Shutdown


## **Handshake** - Header `0x01`
 The message has no payload (it only consists of the header). When the laptop has fully performed intialization steps, it repeatedly sends an initialization message to the Arduino. When the Arduino has performed it's initialization step, it waits to receive the initialization message from the laptop. On receipt, the Arduino will respond with an initialization method signifying that the initialization handshake is complete.