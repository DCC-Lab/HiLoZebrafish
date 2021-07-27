#include <SoftwareSerial.h>
#define rxPin 2
#define txPin 3
SoftwareSerial mySerial(rxPin, txPin); // RX, TX

// Start :
uint8_t dataStart[] = { 0x53, 0x74, 0x61, 0x72, 0x74 };

// Produces a 0x00 crc checksum : 
// DEC : 65, 119, 4, 178, 38, 93
uint8_t dataZero[] = {0x41, 0x77, 0x04, 0xb2, 0x26, 0x93};

// Unpacking is big-endian, therefore the first int received is the lowest byte. 
// Set channel A to sinusoidal waveform : 
// MwSALH. DEC : 77, 119, 83, 65
// Answer : MSALH\r\n. 77, 83, 65, L, H, 13, 10. 
uint8_t dataSin[] = { 0x4D, 0x77, 0x53, 0x41 };

// Reads the channel A current (baseline current  = 292.84 mA)
// CrMAddLH, DEC : 67, 114, 77, 65, 0, 0
// Answer : CMAyyLH\r\n. DEC : 67, 77, 65, smt1, smt2, L, H, 13, 10. 
uint8_t dataCurrent[] = {0x43, 0x72, 0x4D, 0x41, 0x00, 0x00};

// Changes the lower limit of the current range : 
// CwLAxxLH. DEC : 67, 119, 76, 65, HighByte, LowByte
// Answer : CLAxxLH\r\n. DEC : 67, 76, 65, smt1, smt2, L, H, 13, 10.
// 0x00, 0x64 : 100 mA 
// 0x00, 0x7D : 125 mA
// 0x00, 0xC8 : 200 mA
uint8_t dataSetLowerCurrent[] = {0x43, 0x77, 0x4C, 0x41, 0x00, 0x00};

// Reads upper limit of the current range. 
// CrUAddLH. DEC : 67, 114, 85, 65, 0, 0, L, H.
// Answer : CUAyyLH\r\n. DEC : 67, 85, 65, smt1, smt2, L, H, 13, 10.
uint8_t dataReadUpperCurrent[] = {0x43, 0x72, 0x55, 0x41, 0x00, 0x00}; 

// Sets the new output current of a channel, A in this case : 
// AwxxLH. DEC : 65, 119, HighByte, LowByte.
// Answer : None.
// High and Low bytes are a 16bit integer with a value between -4096 and 4096. xi = i0/ic*4096. i0 : Current sent out. ic : 293mA by default.  
// i0 = 200 mA-ish : xi = 2795. HEX : 0x0A, 0xEB. 
// i0 = 100 mA-ish : xi = 1397. HEX : 0x05, 0x75.
// i0 = 50 mA-ish : xi = 699. HEX : 0x02, 0xBB.
uint8_t dataSendCurrent[] = {0x41, 0x77, 0x0A, 0xEB};

// Reads the temperature. 
// TCALH. DEC : 84, 67, 65, L, H. 
// Answer : TCAddLH\r\n. DEC : 84, 67, 65, smt1, smt2, L, H, 13, 10. 
// Convert data to temperature : Temperature [°C] = data * 0.0625 [°C]
uint8_t dataTemp[] = {0x54, 0x43, 0x41};

// Sets the focal power. 
// PwDAxxYYLH. DEC : 80, 119, 68, 65, smt1, smt2, 0, 0, L, H
// Answer : None. 
// High and Low bytes are a 16bit integer with a value between -4096 and 4096. xi = fp *200
// (range of the lens : from -2 to 3) 
// fp = 0, xi = 0. 
// fp = 0.5, xi = 100. (0x00, 0x64)
// fp = 1, xi = 200. (0x00, 0xC8)
// fp = 1.5, xi = 300. 
// fp = 2, xi = 400. 
uint8_t dataFocalPower[] = {0x50, 0x77, 0x44, 0x4B, 0x00, 0x64, 0x00, 0x00};

// Define command : 
byte data[] = {0x41, 0x77, 0x00, 0x00};

void setup() {
// set baud rate for Serial and MySerial : 
Serial.begin(38400);
mySerial.begin(38400);

// define pin modes for rx and tx : 
pinMode(rxPin, INPUT);
pinMode(txPin, OUTPUT);

// Homemade CRC.  
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
Serial.println(newSizeOfArray);
sizeOfArray -= 2;
byte newData[newSizeOfArray] = {0};
int element;
for (element = 0; element < sizeOfArray; ++element) {
 newData[element] = data[element];
 }

// Add CRC to command data :
  // if x is a variable, then &x represents the adress of this variable. Otherwise, if written a & b, it's an AND operator. Only true if both have it. 
  // 0xFF == 255 in decimal. FF_16 == 255_10
newData[sizeOfArray] += crc&0xFF;
Serial.println(newData[sizeOfArray]); 
newData[sizeOfArray+=1] += crc>>8; //sizeOfArray saved the += 1 btw
Serial.println(newData[sizeOfArray]);
 
// Send command : 
//mySerial.write(dataStart, 5);
mySerial.write(newData, newSizeOfArray);
}

void loop() {
Serial.println(mySerial.read());
}

void types(String a) { Serial.println("it's a String"); }
void types(int a) { Serial.println("it's an int"); }
void types(char *a) { Serial.println("it's a char*"); }
void types(float a) { Serial.println("it's a float"); }
void types(bool a) { Serial.println("it's a bool"); }
void types(byte a){Serial.println("it's a byte");}
