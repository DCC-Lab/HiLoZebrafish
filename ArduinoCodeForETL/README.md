# README : Arduino code for HiLo-Zebrafish

This README is made as a list of things to know about the Arduino codes provided in this repository.
The Arduino and the lens driver communicate together with UART communication.

- OneCommandAtATime.ino : Serves only to send one command at a time. So if you send the "Start" command, it will return the "Ready\r\n" command, and that's it. 

- LoopCommandInHiLoSetup.ino : Serves to make volumetric stacks with the HiLo microscope. By setting the step size and the number of images per volume, the driver sends the right amount of current to change the lens curvature to generate the right focal plane change. 

- LensDriverV4Firmware_150617_TypeF_UART.HEX : The firmware that must be installed on the lens driver to make the UART communication available. 

- Optotune Lens Driver 4 software package.zip : Software package. Everything is there to install the lens software (only on Windows) and to install the lens driver firmware. 

  

## How to install the UART firmware:

Follow the normal installation protocol provided when you download the software package from the Optotune website (if it's not available anymore, you can use the one I provide in the repository). It's only when you are at this window that the steps change. 

![Screen Shot 2023-04-19 at 10.44.06 AM](/Users/valeriepineaunoel/Desktop/Screen Shot 2023-04-19 at 10.44.06 AM.png)

To select your custom firmware file, hold Shift + click on Start flashing firmware. A window opens where you can go through your files and select the right .hex file, which is in this case the one provided in the github repository for UART communication. Also, since it's a Type F, change the type for Type F. 


## Description of the two Arduino codes:
All commands used to communication to the lens driver are taken from the specification sheet of the driver (Optotune Lens Driver 4, chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://static1.squarespace.com/static/5d9dde8d550f0a5f20b60b6a/t/63cfdb005b3c212d742d60f8/1674566414045/Optotune+Lens+Driver+4+manual.pdf). 

All commands are converted in hexadecimal values. 

### OneCommandAtATime.ino
This code is used to send one command at a time. Use this one when you start just to make sure that the communication between the Arduino and the lens driver is well done. I recommend sending the "Start" command first, where you should receive "Ready\r\n". 

- The code starts by including the SoftwareSerial library and definine the Rx (receving) and the Tx (transmitting) pins on the Arduino. mySerial is defined afterwards as being the serial communication used to talk to the lens driver. Don't forget that the Tx pin on the Arduino must be connected to the Rx pin on the lens driver and that the Rx pin on the Arduino must be connected to the Tx pin on the lens driver. 

- A few commands in hexadecimal are defined at the beginning of the code for the user. The command that is sent to the lens driver is the one defined by byte data, right before the void setup{} starts. 

- The baud rate must be set at 38 400 bits/second for UART communication with the lens driver (this information is taken directly from the specification sheet). Don't forget to set your baud rate at 38 400 baud in the serial monitor if you need to use it. 

- The pin modes are defined for serial communication with the function pinMode(). 

- The CRC is calculated and then added at the end of the command in the variable byte newData (see section Things to know about the Arduino - lens driver communication: of this README for more information about this). 

- mySerial.write() is used to send the command stored in newData to the lens driver. 

- In the void loop{}, the code only reads what is receives from the lens driver. 

### LoopCommandInHiLoSetup.ino
This code is used when connected to the trigger box, in the HiLo microscope. It basically listens to the input signal from the scrambler (in pin pinInputScrambler) which tells when the trigger box changed the state of the laser speckle reducer (LSR). When the pin pinInputScrambler is at high, it find the right command to send to the lens driver for it to send the correct amount of current to the electrically tunable lens (ETL) to change the focal plane position in z by the amount set in stepSize. When it reaches the number of images set in the variable totalNumberOfImages, it goes backwards. 

- The code starts by including the SoftwareSerial library and definine the Rx (receving) and the Tx (transmitting) pins on the Arduino. mySerial is defined afterwards as being the serial communication used to talk to the lens driver. Don't forget that the Tx pin on the Arduino must be connected to the Rx pin on the lens driver and that the Rx pin on the Arduino must be connected to the Tx pin on the lens driver. 

- We then define what is the low and the high byte in a 16-bits interger. 

- The variable pinInputScrambler defines which digital pin the Arduino listens to the state of the LSR. 

- The user can set the step size in um with the variable stepSize and the total number of planes acquired in a volume with the variable totalNumberOfImages. 

- The variables images, state, dataStart, dataSendCurrent and data MUST NOT BE CHANGED BY THE USER (ideally). 

- In void setup{}, the baud rate is defined at 38 400 bits/second to match to communication speed of the lens driver (this information is taken directly in the specification sheet of the lens driver). The pin modes are defined are outputs or inputs and then the "Start" command is sent. 

- In void loop{}, the Arduino first listens to the state of the pin pinInputScrambler. If pinInputScrambler is at high, it means it is time to change the position of the focal plane, therefore change the ETL curvature, therefore change the current sent to the ETL from the lens driver. To do so, correct value defining the current to the sent by the lens driver to the ETL is calculated using the simple formula provided in the specification sheet ((current/293)*4096) and by identifying the position in Z to go to according to the current position in Z and the step size in um. The low byte and the high byte are identified. 

- Then, the crc is calculated for the current command (see section Things to know about the Arduino - lens driver communication: of this README for more information about the crc). The crc is then added at the end of the command. The command + the crc is saved in the variable newData. 

- mySerial.write() sends the command to the lens driver. This command defines the current that needs to be send to the ETL to change the focal plane position by the amount set by step size. 



## Things to know about the Arduino - lens driver communication: 

- The driver needs a cyclic redundancy check (crc) to confirm that the transmission of the command is done correctly. The crc is a 16-bits number that is calculated for every command and then added at the end of the command as 2 bytes (the low byte is added before the high byte). Therefore, if you want to send the command "Start", the crc is 42474 and the numbers 234 and 165 are added at the end of the command before sending it to the lens driver. 
  

- The Arduino sends serial commands starting from the lowest bit and by framing the byte with start and stop bits. 

  Let's say we want to verify the communication between the Arduino and the lens driver by sending the command "Start" to the lens driver. In binary, this resulsts in sending:

  01010011 01110100 01100001 01110010 01110100 

  The crc check for this commands adds 234 and 165 to the command, which are in binary 11101010 and 10100101, respectively. Therefore, the command in binary becomes:

  01010011 01110100 01100001 01110010 01110100 11101010 10100101

  The Arduino sends the lowest bit first, so the order is inverted, meaning that the Arduino actually sends to the lens driver this command:

  11001010 00101110 10000110 01001110 00101110 01010111 10100101

  with, in addition, a bit defining when the byte starts and 2 bits defining then the bit ends, which are 0 and 11 respectively. Those bits frame every byte. Therefore, if you read the transmitted command "Start" via an oscilloscope sent from the Arduino, you'll read exactly:

  01100101011000101110110100001101100100111011000101110110010101111101010010111
  

- The lens driver answers (when needed) to a command sent by the Arduino by sending back the answer starting from the lowest bit and with each byte framed with a start bit and a stop bit, which are 0 and 1 respectively. 

  From the previous example, if you send "Start" to the lens driver from the Arduino, you'll receive "Ready\r\n". "Ready\r\n" is in binary:

  01010010 01100101 01100001 01100100 01111001 00001101 00001010

  Since the lens driver sends the lowest bit first, every byte is inverted. The bytes then become:

  01001010 10100110 10000110 00100110 10011110 10110000 01010000

  With the start and stop frames every byte. Therefore, if you read the answer sent from the lens driver to the Arduino with an oscilloscope, you'll read:

  001001010101010011010100001101000100110101001111010101100001001010000
  

- If the code doesn't upload to the Arduino Mega (you have an error that looks like *arvdude: stk500v2_ReceiveMessage(): timeout* or *arvdude: butterfly_recv(): programmer is not responding* or something like that), here are things you can try to make it work :

  - Make sure that the board and port are selected for your Arduino in Tools. 
  - Disconnect your Arduino.
  - Close the Arduino IDE. 
  - Reboot the Arduino by clicking on the button by the USB plug. 
  - Use another Arduino Mega. Something might be broken in it. 
  - Test an example code in the File < Examples section. I usually use the Blink one in the 01.Basics section because it doesn't require any connections. If it works, then there is somehting wrong with the ETL code (maybe an update changed the way you have to use a command or something). If it doesn't work, then it's something with the Arduino itself or the connections between the Arduino and the computer. 

  

  
