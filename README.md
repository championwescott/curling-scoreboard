# curling-scoreboard


This is a process to digitize a curling club scoreboard while still maintaining the stardard "hang a card on the board" method for gameplay.

HARDWARE NEEDED (for each scoreboard)
1. Curling scoreboard
<img width="512" height="384" alt="image" src="https://github.com/user-attachments/assets/394396c5-2509-4516-9664-5f75207ced34" />

3. Countersunk magnets (similar to https://www.amazon.com/dp/B095SF6X36?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_22)
4. flathead bolts (head of the bolt should fit inside the magnet hole, and bolt should go through the backof the scoreboard)
5. Wire
6. Printed Circuit Board (PCB)
<img width="1097" height="433" alt="image" src="https://github.com/user-attachments/assets/ee91c68e-4d47-477d-8547-3472dccc4a47" />
<img width="512" height="680" alt="image" src="https://github.com/user-attachments/assets/43b5a954-b3c6-4205-8349-6a52dcd2fa33" />

	5a. microcontroller - D1 mini esp32 (many of the esp32 or es8266 dvices will work, but the PCB was deigned for this footprint)  I am redesigning with an ESP32, as it gives a 12-bit ADC, instead of the 10-bit ADC that the Wemos D1 Mini ESP-12F gives
	
 	5b. 2x 16-channel Analog Multiplexer module (https://www.amazon.com/dp/B07K7JF3HX?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1)

 	5c. 1k ohm resistor

 	5d. 4.7uF capacitor

 	5e. Linear Regulator - I used a TPS76330 to stabilize the voltage level to 3V

 	5f. 17x 1x2 screw terminals
 
8. 6V power supply (4x AA batteries work fine)

9. Hang Cards
    
	Each card needs two pieces of ferrous metal to hang on the magnets
	In between each piece of metal, there needs to be a unique resistor value.
	I used the following:

		Hammer(LSFE) card: 100 ohm

		1st end - 200
   
		2nd - 300
   
		3nd - 400
   
		4th - 500
   
		5th - 600
   
		6th - 700
   
		7th - 800
   
		8th - 900
   
		9th - 1000
   
		10th - 1100
   
	
The basic idea behind this is as follows: a 3V voltage signal is output from the PCB and runs to the first magnet of each hang card spot on the scoreboard.  The second magnet i wired to the corresponding screw terminal on the PCB.

When a card is hung, the voltage signal travels through the resistor (R1) on the hang card, and back to the screw terminal on the PCB.  Each screw terminal is connected to an input on the 16-to-1 analog multiplexer.

<img width="286" height="336" alt="image" src="https://github.com/user-attachments/assets/85f7c05f-3734-4e71-8a66-59a16dd81b38" />

The output of the multiplexer is connected to the Analog input port on the microcontroller (Vout) and then also across the 2 resistor (1k ohm) which is conneted to ground.  The output voltage is measured by the ADC of the microcontroller according to the followin formula:

<img width="276" height="121" alt="image" src="https://github.com/user-attachments/assets/c710c5ce-913b-4f9b-b654-49d2d827ecf3" />

Then we can calculate the value of R1, and determine which card was hung on the scoreboard.

The code will loop through each input on the multiplexers (first one, then the second), compare the measured resistances with set values, record which cards are hung where, and then update a database over MQTT.

I don't have a picture of the internal of the scoreboard, but it was a lot of wires.  32 wires for each rock color.


CODE
The python scripts are fairly basic.  

"scoreboard_backend.py" will monitor the MQTT topic and write the received JSON output to a file.

"scoreboard_frontend.py" will read tha file, and display an updating, textbased scoreboard.

"scoreboard-code.ino" is the firmware for the microcontroller.  Should be able to compile and load it from an Arduino IDE.  I am also working on an ESPHome configuration.
