# Arduino-Laptop Communication Protocol

## Message Header

Each message will be proceeded by a header byte specifying what data is being sent. The length of the message will be fixed for each message type.

* 0x01 - Initialization Handshake
* 0x02 - Move Chess Piece
* 0x04 - Button pressed, player has made move
* 0x08 - Command received confirmation
* 0x10 - Reset
* 0x20 - Shutdown