#include <SoftwareSerial.h>

// UART communication with the lens driver : 
#define rxPin 2
#define txPin 3
SoftwareSerial mySerial(rxPin, txPin); // RX, TX

// Access the high and low bytes of a 16-bits integer : 
#define LOWBYTE(variable)   ((unsigned char) (variable))
#define HIGHBYTE(variable)  ((unsigned char) (((unsigned int) (variable)) >> 8))

// pin that receives the signal form the scrambler : 
int pinInputScrambler = 10;

// Set step size (axial shift) of the volume [um] : 
int stepSize = 3;

// Number of HiLo images per volume : 
int totalNumberOfImages = 180;
int image = 1;

// Keep in memory the axial shift (z position of the focal plane compared to the initial z position) in time : 
int positionInZ = 0;

// Some variable that retains the changes in the state of the received signal from the scrambler : 
int state = false;

// Commands : 
// Start :
uint8_t dataStart[] = { 0x53, 0x74, 0x61, 0x72, 0x74 };
// Sets the new output current of a channel, A in this case : 
// AwxxLH. DEC : 65, 119, HighByte, LowByte.
// Answer : None.
// High and Low bytes are a 16bit integer with a value between -4096 and 4096. xi = i0/ic*4096. i0 : Current sent out. ic : 293mA by default.  
// i0 = 200 mA-ish : xi = 2795. HEX : 0x0A, 0xEB. 
// i0 = 100 mA-ish : xi = 1397. HEX : 0x05, 0x75.
// i0 = 50 mA-ish : xi = 699. HEX : 0x02, 0xBB.
uint8_t dataSendCurrent[] = {0x41, 0x77, 0x0A, 0xEB};

// Define command to be sent : 
byte data[] = {0x41, 0x77, 0x00, 0x00};

void setup() {
// set baud rate for Serial and MySerial :
Serial.begin(38400);
mySerial.begin(38400);

// define pin modes for rx and tx : 
pinMode(pinInputScrambler, INPUT);
pinMode(rxPin, INPUT);
pinMode(txPin, OUTPUT);

// Send Start command : 
mySerial.write(dataStart, 5);
}

void loop() {
  // Read pin of scrambler : 
  int scramblerVal = digitalRead(pinInputScrambler);
  
  // Transition LOW to HIGH : 
  if (scramblerVal == HIGH && state == false) {
  // manque un boutte pour dire c'est quoi la commande à partir de 0
  // High and Low bytes are a 16bit integer with a value between -4096 and 4096. xi = i0/ic*4096. i0 : Current sent out. ic : 293mA by default.

  // Calculates the value of current to be sent : 
  float current = 0.63484 + 0.14365*positionInZ + (-7.6613E-5)*pow(positionInZ, 2) + 6.7508E-8*pow(positionInZ, 3) + (-4.0543E-11)*pow(positionInZ, 4) + 9.3762E-15*pow(positionInZ, 5);
  // Calculates the integer to be sent in the command to change the current. int stores a 16-bits value on Arduino Uno.
  int valueInCommand = (current/293)*4096; // va toujours arrondir vers le bas
  // Store High and Low bytes in a byte variable because it is too dumb to do it by itself:
  byte Hi = HIGHBYTE(valueInCommand);
  byte Lo = LOWBYTE(valueInCommand);
  // Replace the last and the one-before-the-last bytes of the command data by the Hi and Low bytes :
  data[sizeof(data)-2] = Hi;
  data[sizeof(data)-1] = Lo;

  //Homemade CRC : 
  uint16_t crc = 0, i;
  for (i = 0; i < sizeof(data) / sizeof(data[0]); i++) { // i++ increments the value of i without changing the value of i
    uint8_t a = data[i];
    crc ^= a; // addition of a to crc
    int l;
  
  for (l = 0; l < 8; ++l){
    if (crc & 1) { // and operant. Both must be true or 1. 
    crc = (crc >> 1) ^ 0xA001; // ^ : do the thing if it is in one operant, but not both. 
    }else{
    crc = (crc >> 1); // >> : the bits of the left operand to be shifted left by the number of positions specified by the right operand.
        }
    }
  }

  // Create new array of data because it's too dumb to increase its size by its own. 
  int sizeOfArray = sizeof(data) / sizeof(data[0]);
  int newSizeOfArray = sizeOfArray += 2;
  sizeOfArray -= 2;
  uint8_t newData[newSizeOfArray] = {0};
  int element;
  for (element = 0; element < sizeOfArray; ++element) {
    newData[element] = data[element];
    }

  // Add CRC to command data : Comprendre ça ici! Je pense peut-être que c'est ça qui chie #2. 
  // if x is a variable, then &x represents the adress of this variable. Otherwise, if written a & b, it's an AND operator. Only true if both have it. 
  // 0xFF == 255 in decimal. FF_16 == 255_10
  newData[sizeOfArray] += crc&0xFF; 
  newData[sizeOfArray+=1] += crc>>8; //sizeOfArray saved the += 1 btw

  // Send command : 
  mySerial.write(newData, newSizeOfArray);

  // Increment the axial shift of one step size : 
  positionInZ += stepSize;
  image += 1;

// When the z-stack is done: 
  if (image <= 1 || image >= totalNumberOfImages) {
    positionInZ = 0; // Retourner au plan de départ, à current = 0 mA
    // stepSize = -stepSize; // Revirer de bord quand il atteint son maxDepth
    image = 1;
    }
  
  state = true;
    }
  
  // Transition HIGH to LOW : 
  if (scramblerVal == LOW && state == true) {
    state = false; 
    }
    
  else {} // waiting
}
