# MicroBaller_Controller

When using for the first time:
- Find the peripheral_address section in main.py
- If you know your ESP's bluetooth MAC address 
  - Replace the existing one with the one for your ESP
- If not 
  - Turn on the ESP with its program running (LED Flashing)
  - Run BT_Scaner.py
  - Once its finished, find the line with the name MicroBaller
  - Copy everything in the line, up to, but not including, the colon and replace the existing address in main.py
- If you are using a different controller to the Xbox one controller then create a new constants file for it and change the import in main from Xbox_One_Constants to your new file
- That should be it

To Run:
- Start the ESP first to create the server
- Then run main.py
- Wait for the terminal to indicate the client is connected anf the joystick is detected 
- The gatt client on the computer should now be connected to the ESP and should be sending the controller data across to the ESP 

ESP_Bluetooth:
- In the ESP_Bluetooth directory is main.py. main.py is the working micropython file that starts the server and reads the messages from the client decoding them back to an integer list with joystick/trigger values 0 to 256 and button values 0 or 1