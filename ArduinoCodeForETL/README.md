# README : Arduino code for HiLo-Zebrafish

This README is made as a list of things to know about the Arduino codes provided in this repository.
All commands used are taken from the specification sheet of the driver (Optotune Lens Driver 4, chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://static1.squarespace.com/static/5d9dde8d550f0a5f20b60b6a/t/63cfdb005b3c212d742d60f8/1674566414045/Optotune+Lens+Driver+4+manual.pdf). 
The Arduino and the lens driver communicate together with UART communication.

- OneCommandAtATime.ino : Serves only to send one command at a time. So if you send the "Start" command, it will return the "Ready\r\n" command, and that's it. 

- LoopCommandInHiLoSetup.ino : Serves to make volumetric stacks with the HiLo microscope. By setting the step size and the number of images per volume, the driver sends the right amount of current to change the lens curvature to generate the right focal plane change. 

- LensDriverV4Firmware_150617_TypeF_UART.HEX : The firmware that must be installed on the lens driver to make the UART communication available. 

- Optotune Lens Driver 4 software package.zip : Software package. Everything is there to install the lens software (only on Windows) and to install the lens driver firmware. 

  

## How to install the UART firmware:

Follow the normal installation protocol provided when you download the software package from the Optotune website (if it's not available anymore, you can use the one I provide in the repository). It's only when you are at this window that the steps change. 

![Screen Shot 2023-04-19 at 10.44.06 AM](/Users/valeriepineaunoel/Desktop/Screen Shot 2023-04-19 at 10.44.06 AM.png)

To select your custom firmware file, hold Shift + click on Start flashing firmware. A window opens where you can go through your files and select the right .hex file, which is in this case the one provided in the github repository for UART communication. Also, since it's a Type F, change the type for Type F. 



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

  - Disconnect your Arduino.
  - Close the Arduino IDE. 
  - Reboot the Arduino by clicking on the button by the USB plug. 
  - Use another Arduino Mega. Something might be broken in it. 
  - Test an example code in the File < Examples section. I usually use the Blink one in the 01.Basics section because it doesn't require any connections. If it works, then there is somehting wrong with the ETL code (maybe an update changed the way you have to use a command or something). If it doesn't work, then it's something with the Arduino itself or the connections between the Arduino and the computer. 

  

  