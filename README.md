# curling-scoreboard


This is a process to digitize a curling club scoreboard while still maintaining the stardard "hang a card on the board" method for gameplay.

HARDWARE NEEDED (for each scoreboard)
1. Curling scoreboard (picture here)
2. Countersunk magnets (similar to https://www.amazon.com/dp/B095SF6X36?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_22)
3. flathead bolts (head of the bolt should fit inside the magnet hole, and bolt should go through the backof the scoreboard)
4. Wire
5. Printed Circuit Board (PCB) 
	5a. microcontroller - D1 mini esp32 (many of the esp32 or es8266 dvices will work, but the PCB was deigned for this footprint)  I am redesigning with an ESP32, as it gives a 12-bit ADC, instead of the 10-bit ADC that the Wemos D1 Mini ESP-12F gives
	5b. 2x 16-channel Analog Multiplexer module (https://www.amazon.com/dp/B07K7JF3HX?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1)
	5c. 1k ohm resistor
	5d. 4.7uF capacitor
	5e. Linear Regulator - I used a TPS76330 to stabilize the voltage level to 3V
	5f. 17x 1x2 screw terminals
6. 6V power supply (4x AA batteries ork fine)
6. Hang Cards
	Each card needs two pieces of ferrous metal to hang on the magnets
	In between each piece of metal, there needs to be a unique resisor value.
	I used teh following:
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
