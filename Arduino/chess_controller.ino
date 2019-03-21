#define INIT_HANDSHAKE_HEADER 0x01

int incomingByte = 0;


//Perform initialization handshake signifying Arduino is ready to begn
// Waits until init handshake is received from laptop before proceeding
void initHandshake()
{
  // Read in received data
  int receivedData = 0;

  // Loop waiting for laptop to send initialization handshake message
  while(receivedData != 1)
  {
    receivedData = Serial.read();
  }
  Serial.write(INIT_HANDSHAKE_HEADER);
  Serial.write(INIT_HANDSHAKE_HEADER);
}

void setup() {


}

void loop() {

}
